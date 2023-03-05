import re
import httpx
import asyncio
import requests 

from pyrogram import Client, filters
from pyrogram.types import Message

from TelegramBot.config import SUDO_USERID
from TelegramBot import NZBHYDRA_URL_ENDPOINT  
from TelegramBot.usenetbot.sabnzbd import UsenetBot 
from TelegramBot.helpers.filters import check_auth, sudo_cmd

sabnzbd_userid_log: dict = {} #saves userid of user along with his task id. {userid:[task1, task2]}
    
    
usenetbot = UsenetBot () 
@Client.on_message(filters.command("pstatus") & check_auth)
async def downloading_status(client: Client, message: Message):
    await usenetbot.show_postprocessing_status(client, message)
    
    									    									    									
@Client.on_message(filters.command(["status", "dstatus"]) & check_auth)
async def postprocessing_status(client: Client, message: Message):
    await usenetbot.show_downloading_status(client, message)
    
    
@Client.on_message(filters.command(["resumeall", "pauseall", "cancelall"]) & sudo_cmd)
async def sudo_cmds(client: Client, message: Message):
    
    command = message.command[0]    
    if command == "resumeall":
    	if usenetbot.resumeall_task():
            return await message.reply_text("Resumed all Task successfully.", quote= True)
          
    elif command == "pauseall":
    	if usenetbot.pauseall_task():
            return await message.reply_text("Paused all Task successfully.", quote=True)
            
    elif command == "cancelall":
    	if usenetbot.deleteall_task():
            return await message.reply_text("Cancelled all Task successfully.", quote=True)
            
    return await message.reply_text("something went wrong.", quote=True)    
         	                                                                               
                                                                                    
                                        
@Client.on_message(filters.command("resume") & check_auth)
async def resume_task(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Send Task ID with the command to resume the Task.")
    
    user_id, user_input = message.from_user.id, message.text.split(None, 1)[1]
    if (user_id not in sabnzbd_userid_log) and (user_id not in SUDO_USERID):
    	return await message.reply_text("No Task found under your User ID.", quote=True)
    
    if user_id not in SUDO_USERID:
    	if user_input not in sabnzbd_userid_log[user_id]:
    		return await message.reply_text("No Task found with that Task ID under your User ID.", quote=True)
    	
    result = usenetbot.resume_task(task_id=user_input)
    if result:
    	return await message.reply_text(f"Task {user_input} successfully resumed.", quote=True)
    else: return await message.reply_text("No Task found with that Task ID .", quote=True)
   
   
   
@Client.on_message(filters.command("pause") & check_auth)
async def pause_task(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Send Task ID with the command to  the Task.")
    
    user_id, user_input = message.from_user.id, message.text.split(None, 1)[1]  
    if (user_id not in sabnzbd_userid_log) and (user_id not in SUDO_USERID):
    	return await message.reply_text("No Task found under your User ID.", quote=True)
    
    if user_id not in SUDO_USERID:
    	if user_input not in sabnzbd_userid_log[user_id]:
    		return await message.reply_text("No Task found with that Task ID under your User ID.", quote=True)
    	
    result = usenetbot.pause_task(task_id=user_input)
    if result:
    	return await message.reply_text(f"Task {user_input} successfully paused.", quote=True)
    else: return await message.reply_text("No Task found with that Task ID .", quote=True)
   
 
           	  	       	  		          	  	       	  		
@Client.on_message(filters.command(["delete", "cancel"]) & check_auth)
async def delete_task(client: Client, message: Message):
    
    if len(message.command) < 2:
        return await message.reply_text("Send Task ID with the command to delete the Task.")
    
    user_id, user_input = message.from_user.id, message.text.split(None, 1)[1]
    if (user_id not in sabnzbd_userid_log) and (user_id not in SUDO_USERID):
    	return await message.reply_text("No Task found under your User ID.", quote=True)
    
    if user_id not in SUDO_USERID:
    	if user_input not in sabnzbd_userid_log[user_id]:
    		return await message.reply_text("No Task found with that Task ID under your User ID.", quote=True)
    	
    result = usenetbot.delete_task(task_id=user_input)
    if result:
    	return await message.reply_text(f"Task {user_input} successfully deleted.", quote=True)
    	
    else: return await message.reply_text("No Task found with that Task ID .", quote=True)
   


@Client.on_message(filters.command("nzbmirror") & check_auth)
async def nzbmirror(client: Client, message: Message):
    
    userid = message.from_user.id
    replied_message = message.reply_to_message
    
    if not replied_message:
    	return await message.reply_text("Reply to a proper NZB file to mirror.", quote=True)    	
    
    replymsg  = await message.reply_text("Adding your NZB file. Please Wait...",  quote=True)
    if not replied_message.document:
    	return await replymsg.edit("Reply to a proper NZB file to mirror.")
    
    if not all([bool(replied_message.document), ".nzb" in replied_message.document.file_name]):
    	return await replymsg.edit("Reply to a proper NZB file to mirror.")
    	
    download_path = await message.reply_to_message.download()    
    result = await usenetbot.add_nzbfile(path_name=download_path)    
       
    if result["status"]:
    	sabnzbd_userid_log.setdefault(userid, []).append(result["nzo_ids"][0])        	
    	asyncio.create_task(usenetbot.show_downloading_status(client, message))
    	return await replymsg.edit("Your NZB file is successfuly Added in Queue.")        		        		
    return replymsg.edit("Something went wrong while processing your NZB file.")
    

        
@Client.on_message(filters.command(["nzbgrab", "nzbadd"]) & check_auth)
async def nzbgrab(client: Client, message: Message):
    
    userid = message.from_user.id 
    if len(message.command) < 2:
    	return await message.reply_text("Please provide a proper ID", quote=True)
    	
    user_input = message.text.split(maxsplit=1)[1]    
    nzbhydra_idlist = re.findall(r"-?\b[0-9]+\b", user_input)    
    
    if not nzbhydra_idlist:
    	return await message.reply_text("Please provide a proper ID.", quote=True)
    	
    replymsg  = await message.reply_text("Adding your requested ID(s). Please Wait...",  quote=True)
    
    success_taskids = []
    for id in nzbhydra_idlist:
        nzburl = NZBHYDRA_URL_ENDPOINT.replace("replace_id", id)
        async with httpx.AsyncClient() as client:
        	response = await client.head(nzburl)
        
        if "Content-Disposition" in response.headers:
        	result = usenetbot.add_nzburl(nzburl)
        
        if result["status"]:
        	success_taskids.append(result['nzo_ids'][0])

       		
    if success_taskids:
        sabnzbd_userid_log.setdefault(userid, []).extend(success_taskids)
        asyncio.create_task(usenetbot.show_downloading_status(client, message))
        
        await replymsg.delete()
        return await message.reply_text(f"{len(success_taskids)} Tasks have been successfully added.", quote=True)
       
    return await replymsg.edit("No task has been added.")
       	
