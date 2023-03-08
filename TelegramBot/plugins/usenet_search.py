import re
import requests

from pyrogram import Client, filters
from pyrogram.types import Message
from typing import Callable, Union

from TelegramBot.usenetbot.nzbhydra import NzbHydra
from TelegramBot.helpers.filters import check_auth, sudo_cmd
from TelegramBot.helpers.pasting_services import katbin_paste, telegraph_paste 


def errors(func: Callable) -> Callable:
    @wraps(func)
    async def decorator(client, message, *args,**kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except Exception as error:
            await message.reply("Something went wrong. Please Try again later.")

    return decorator
    

nzbhydra = NzbHydra()
@Client.on_message(filters.command(["nzbfind", "nzbsearch", "movie", "series", "tv"]) & check_auth)
@errors
async def search(_, message: Message):

	if len(message.command) < 2:
		return await message.reply_text("Please provide a proper search query.", quote=True)

	user_input= message.text.split(maxsplit=1)[1]
	reply_msg= await message.reply_text("Searching your query. Please wait...", quote=True)

	output = ""
	command = message.command[0]
	if command in ["nzbfind", "nzbsearch"]:
		output = await nzbhydra.query_search(user_input)

	elif command in ["movie", "movies"]:
		if re.search("^tt[0-9]*$", user_input):
			output = await nzbhydra.imdb_movie_search(user_input)

		elif imdbid := re.search(r".+(tt\d+)", user_input):
			try: output = await nzbhydra.imdb_movie_search(imdbid.group(1))
			except: output = await nzbhydra.movie_search(user_input)

		else: output = await nzbhydra.movie_search(user_input)


	elif command in ["series", "tv"]:
		if re.search("^tt[0-9]*$", user_input):
			output = await nzbhydra.imdb_series_search(user_input)

		elif imdbid := re.search(r".+(tt\d+)", user_input):
			try: output = await nzbhydra.imdb_series_search(imdbid.group(1))
			except: output = await nzbhydra.series_search(user_input)

		else: output = await nzbhydra.series_search(user_input)

	if output:
		telegraph_output = await telegraph_paste(output)
		return await reply_msg.edit(f"Search Query: `{user_input}`\n\n{telegraph_output}", disable_web_page_preview=False)

	return await reply_msg.edit("Nothing Found.")


@Client.on_message(filters.command(["indexers"]) & sudo_cmd)
async def indexer_list(_, message: Message):
	"""List all the connected indexers."""
	
	replymsg = await message.reply_text("Fetching list....", quote=True)
	indexers = await nzbhydra.list_indexers()
	
	if indexers:
		return await replymsg.edit(indexers)

	return await replymsg.edit("No indexers found.")

