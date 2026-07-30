## ##
##
##    One-off maintenance script.
##
##    This bot only registers guild-scoped slash commands, so any GLOBAL commands
##    registered by an older version of your application stay in Discord forever
##    and show up as duplicates that answer "The application did not respond".
##
##    Run this once to delete every global command of your application:
##        python clear_global_commands.py
##
##    On Railway: Settings -> Deploy -> Custom Start Command ->
##    `python clear_global_commands.py`, redeploy once, then remove it again.
##
## ##

import discord, json, os
from discord import app_commands

config = json.load(open('config.json'))
if os.getenv("DISCORD_TOKEN"):
    config["token"] = os.getenv("DISCORD_TOKEN")

bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


@bot.event
async def on_ready():
    existing = await tree.fetch_commands()
    print(f"Found {len(existing)} global command(s): {[c.name for c in existing]}")

    tree.clear_commands(guild=None)
    await tree.sync()

    print("Deleted all global commands. Guild commands were not touched.")
    print("Reset your start command back to `python main.py` and redeploy.")
    await bot.close()


bot.run(config['token'])
