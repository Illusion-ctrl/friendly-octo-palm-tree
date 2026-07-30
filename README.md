# Account Generator Bot
### THIS PROGRAM DOES NOT MAKE ACCOUNTS FOR YOU.
A discord bot which manages a database of accounts and provides a user-friendly way to retrive them. Users can generate them thru an command and receive the account in their DMs. The bot ensures that each account is only distributed once, keeping the process organized and efficient.

# Commands
Parameters marked with a star(*) are required.
* `/addstock *[service] *[txt_file] [is_premium] [is_silent]` - Adds your lines to the database.
* `/panel` - Admin only. Posts the gen panel (Free Gen / Premium Gen / Stock buttons) in the current channel.
* `/rebuildserver [delete_other_channels]` - Admin only. Creates the categories and channels from `server-template` in the config. Asks for confirmation first.
* `/branding` - Admin only. Applies `theme.bot-username` and `theme.bot-avatar-url` to the bot.
* `/blacklist *[user] [status]` - Blacklist the user from using /gen.
* `/bulkgen *[service] *[amount] *[is_premium] [is_silent]` - Admin only. Generate multiple accounts at a time.
* `/clearservice *[service] [is_premium]` - Clear all lines from a specific stock.
* `/cooldown reset *[user] [stage]` - Resets their current cooldown. (not custom cooldown)
* `/cooldown set *[user] *[stage] [time_sec] [is_silent]` - Sets a custom cooldown for the user.
* `/gen *[service] [is_premium]` - Gets a random line from the database and sends it to the user.
* `/setnote *[user] *[note]` - Set a custom note for the user, u can see it when doing /user [user]
* `/stock` - See, how many lines are in the database.
* `/subscription add *[user] *[time_sec] [is_silent]` - Admin only. Add time to user's subscription.
* `/subscription massadd *[time_sec] [is_silent]` - Admin only. Extend everyones subscription. (only people who had a sub)
* `/subscription remove *[user] [is_silent]` - Admin only. Remove users subscription.
* `/subscription set *[user] *[time_sec] [is_silent]` - Admin only. Set users premium subscription.
* `/subscription view [user] [is_silent]` - View your(user only) or other people's(admin only) subscription.
* `/user *[user]` - Admin only. View info about user.


# How to setup
Having problems setting it up? You can contact me in discord. If I'm free I can help you with setup.

(This tutorial might be missing some stuff, if i forgot something)
### 1. INSTALLING PYTHON (dont skip)
First of all make sure you have python installed (3.11.6 recommended) on the machine you want to host the bot on. (Yes, you have to host the bot yourself. There is **NO** invite link.).
When installing python, make sure to enabled 'ADD TO PATH' in the installer. If you have multiple versions of python installed, uninstall all of them and install 3.11.6 from [PYTHON](https://www.python.org/downloads/release/python-3116/)

### 2. DOWNLOADING THE SOURCE
Download all the files in the github. **DO NOT** edit any of the .py files (if you don't know what you're doing). Everything you want/need to edit is inside the config.json file.

### 3. INSTALLING THE MODULES. (!)
Open an console in the directory where the source is at and run the command: `pip install -r requirements.txt`

### 4. CONFIG (!)
In the config you need to put your **DISCORD BOT TOKEN** not your account token, which u can get from the [Discord Developer Portal](https://discord.com/developers/docs/). You make the bot and then go to the **BOT** tab and click on reset token, it will ask for password or code if you have mfa on your discord account. After confirming, copy the token and put it in your config. To get the guild-id aka your server id you need to enable developer mode in discord and right clicking on your server icon -> copy server id. Fill out the gen-channels, premium-gen-channels, admin-roles and the roles. You can also edit the footer message and the dm message in the config.

### 5. INVITING THE BOT
You can invite it from the Discord Developer Portal. Choose the bot you want to invite. Go to OAuth2 tab. Scroll down to 'OAuth2 URL Generator'. Enable 'bot' and 'applications.commands'. An invite link gets generated at the bottom. Copy it and open it in a new tab.
Invite the bot to your server. Now you can run the main.py file.


# Panel, theming and server template

### Gen panel
Run `/panel` in the channel you want it in. It posts an embed with **Free Gen**, **Premium Gen** and
**Stock** buttons; clicking one opens a private service picker and the account is DM'd as usual.
The panel keeps working after restarts and never goes stale, because the service list is built when
the button is pressed instead of being baked into the message. All the normal checks still apply, so
the panel has to live in one of your `gen-channels` (or you have to have an admin role).

### Theming
The `theme` section of config.json controls the branding:

| Key | What it does |
| --- | --- |
| `bot-username` | Renamed on startup when it differs. Discord allows 2 renames per hour. |
| `bot-avatar-url` | Direct link to a png/jpg. Applied by `/branding` (not on every restart, to avoid rate limits). |
| `server-name` | Renames the server during `/rebuildserver`. Leave empty to skip. |
| `panel-title`, `panel-description`, `panel-image-url`, `panel-thumbnail-url` | The panel embed. |
| `service-emoji` | Emoji shown next to each service in the picker. |

`messages.altsent`, `messages.footer-msg`, `colors` and `generate-settings.gif-img-url` still work
the same way - set `gif-img-url` to `""` if you don't want a gif on the gen message.

### Server template
`server-template` in config.json is the layout `/rebuildserver` builds:

```json
{
    "name": "G3N",
    "channels": [
        {"name": "free-gen"},
        {"name": "premium-gen", "private": true, "roles": [ROLE_ID]}
    ]
}
```

* `private: true` hides the channel (or whole category) from `@everyone` and allows `admin-roles`.
* `roles` grants extra role ids access on top of the admins.
* Channels that already exist are skipped, so running it twice is harmless.
* `delete_other_channels: true` deletes every channel **not** in the template - the channel you ran
  the command in is always kept.

The bot needs **Manage Channels** (and **Manage Server** if you set `server-name`).

### Who can use the admin commands
`/panel`, `/rebuildserver` and `/branding` require **Manage Server**, so Discord hides them from
normal members instead of just refusing them. On top of that the bot still checks `admin-roles`.
To allow a staff role that doesn't have Manage Server, go to
`Server Settings -> Integrations -> your bot` and add a permission override per command.

# Hosting on Railway

The repo is ready to deploy on [Railway](https://railway.app) as a worker (no web port needed).

### 1. Fill out config.json and push it
Everything except the token and the server id is read from `config.json`, so set `gen-channels`,
`premium-gen-channels`, `admin-roles`, `roles` etc. and commit them. Leave `token` as the
placeholder - it is supplied by an environment variable instead so your token never ends up in git.

### 2. Create the Railway service
`New Project` -> `Deploy from GitHub repo` -> pick this repo. Railway detects Python via Nixpacks,
installs `requirements.txt`, and starts `python main.py` (see `railway.json` / `Procfile`).

### 3. Set the variables
In the service's `Variables` tab (see `.env.example`):

| Variable | Required | Description |
| --- | --- | --- |
| `DISCORD_TOKEN` | yes | Your bot token. Overrides `token` in config.json. |
| `GUILD_ID` | no | Your server id. Overrides `guild-id` in config.json. |
| `DATABASE_PATH` | recommended | Path of the SQLite file, e.g. `/data/database.db`. |

### 4. Add a volume (important)
The bot stores stock, users, cooldowns and subscriptions in SQLite. Railway containers have an
ephemeral filesystem, so without a volume **your database is wiped on every redeploy**.
In the service, `Settings` -> `Volumes` -> `Add volume` with mount path `/data`, then set
`DATABASE_PATH=/data/database.db`.

### 5. Deploy
Redeploy and check the `Deploy Logs` - you should see `Logged in as ...`. If Railway shows the
service as crashed, the logs will usually show either an invalid token or missing intents
(see the Errors section below).

# Errors

If you get any errors that are not listed here feel free to contact me in discord, you can get my discord from my github profile.

### 1. Privileges/intents
Go to https://discord.dev and enable all the intents for your application. (discord.dev -> applications -> choose your application -> bot -> scroll down a bit -> there should be 'Privileged Gateway Intents' -> enable all)

### 2. Not sending messages
Make sure your intents are enabled and the bot has permission to send messages in the channel you're using the bot in. (You also have to specify the channels where the generate command can be used in thru the config). If the bot doesn't send a DM then make sure your dms are open.

### 4. Addstock doesn't work
It takes each line as an account from the txt file, so each account has to be on a seperate line.

Example of an txt file (it can be any of those):
```
account@gmail.com:test
tester:hello|capture
or just a piece of text
```
