import re
import requests 

from pyrogram import Client, filters
from pyrogram.types import Message
 
from TelegramBot.usenetbot.nzbhydra import NzbHydra 
from TelegramBot.helpers.filters import check_auth, sudo_cmd
from TelegramBot.helpers.pasting_services import katbin_paste


nzbhydra = NzbHydra()	
@Client.on_message(filters.command(["search", "nzbsearch", "movie", "series", "tv"]) & check_auth)
async def search(_, message: Message):   

    if len(message.command) < 2:
    	return await message.reply_text("Please provide a proper search query.", quote=True)
    	
    user_input= message.text.split(maxsplit=1)[1]    
    reply_msg= await message.reply_text("Searching your query. Please wait...", quote=True)
    
    output = ""
    command = message.command[0]
    if command in ["search", "nzbsearch"]:
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
    	telegraph_output = await katbin_paste(output)
    	return await reply_msg.edit(telegraph_output, disable_web_page_preview=True)   
    		
    return await reply_msg.edit("Nothing Found.")
                    			
	
@Client.on_message(filters.command(["indexers"]) & sudo_cmd)
async def indexer_list(_, message: Message):
	indexers = await nzbhydra.list_indexers()
	if indexers:
		return await message.reply_text(indexers, quote=True)
	
	return await message.reply_text("No indexers found.", quote=True)

