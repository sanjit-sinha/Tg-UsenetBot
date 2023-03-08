from TelegramBot.version import (__python_version__, __version__, __pyro_version__, __license__)

COMMAND_TEXT = """
🗒️ Documentation for commands available to user's

• /nzbfind - Search your query.
• /movie - Search by movie name / Imdb ID / Imdb link.
• /series - Search by series name / Imdb Id / Imdb link.

• /status - Get status message of downloading and post processing.
• /serverstats - Get detailed stats of the server.
• /nzbgrab - Add NZB IDs to download.
• /nzbmirror - Mirror .nzb file.
• /resume - Resume the task.
• /pause - Pause the task.
• /cancel - Cancel the task.
"""


ABOUT_CAPTION = f"""• Python version : {__python_version__}
• Bot version : {__version__}
• pyrogram  version : {__pyro_version__}

**Github Repo**: https://github.com/sanjit-sinha/TelegramBot-UsenetBot"""

START_ANIMATION = "https://telegra.ph/file/c0857672b427bec8542f6.mp4"

START_CAPTION = """Hello there! I am a Telegram bot designed to help you control your SABnzbd and NZBHydra instances via Telegram to easily manage your downloads, see their progress, search for new content, and much more!  \n\nUse buttons to navigate and know more about me :)"""

COMMAND_CAPTION = """**Here are the list of commands which you can use in bot.\n**"""
