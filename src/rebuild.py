import discord


def normalize(name: str):
    """Discord lowercases channel names and turns spaces into dashes, so a
    template entry has to be compared against the normalized form."""
    return name.strip().lower().replace(" ", "-")


def build_overwrites(guild: discord.Guild, entry: dict, admin_role_ids: list):
    if not entry.get("private") and not entry.get("roles"):
        return {}

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False)
    }
    for role_id in list(admin_role_ids) + list(entry.get("roles", [])):
        role = guild.get_role(int(role_id))
        if role is not None:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True)
    return overwrites


async def apply_template(
    guild: discord.Guild,
    template: list,
    admin_role_ids: list,
    delete_existing: bool = False,
    protected_channel_id: int = None,
):
    """Creates every category/channel of the template that is missing.

    Existing channels are left untouched so running this twice is safe. With
    delete_existing every channel that is not part of the template is removed,
    except protected_channel_id (the channel the command was invoked from).
    """
    report = {"created": [], "existing": [], "deleted": [], "failed": []}
    wanted_channels = set()

    for category_entry in template:
        category_name = category_entry["name"]
        category = discord.utils.find(
            lambda c: normalize(c.name) == normalize(category_name), guild.categories
        )
        if category is None:
            try:
                category = await guild.create_category(
                    category_name,
                    overwrites=build_overwrites(guild, category_entry, admin_role_ids),
                    reason="Server rebuild",
                )
                report["created"].append(category_name)
            except discord.HTTPException as error:
                report["failed"].append(f"{category_name}: {error}")
                continue
        else:
            report["existing"].append(category_name)

        for channel_entry in category_entry.get("channels", []):
            channel_name = channel_entry["name"]
            wanted_channels.add(normalize(channel_name))

            channel = discord.utils.find(
                lambda c: normalize(c.name) == normalize(channel_name), guild.text_channels
            )
            if channel is not None:
                report["existing"].append(channel_name)
                continue

            try:
                await guild.create_text_channel(
                    channel_name,
                    category=category,
                    topic=channel_entry.get("topic"),
                    overwrites=build_overwrites(guild, channel_entry, admin_role_ids),
                    reason="Server rebuild",
                )
                report["created"].append(channel_name)
            except discord.HTTPException as error:
                report["failed"].append(f"{channel_name}: {error}")

    if delete_existing:
        for channel in list(guild.text_channels):
            if normalize(channel.name) in wanted_channels:
                continue
            if protected_channel_id is not None and channel.id == protected_channel_id:
                continue
            try:
                await channel.delete(reason="Server rebuild")
                report["deleted"].append(channel.name)
            except discord.HTTPException as error:
                report["failed"].append(f"{channel.name}: {error}")

        template_categories = {normalize(c["name"]) for c in template}
        for category in list(guild.categories):
            if normalize(category.name) in template_categories or category.channels:
                continue
            try:
                await category.delete(reason="Server rebuild")
                report["deleted"].append(category.name)
            except discord.HTTPException as error:
                report["failed"].append(f"{category.name}: {error}")

    return report
