import re
import time
import httpx
import aiofiles
import asyncio
import requests
import urllib.parse

from shutil import disk_usage
from datetime import datetime
from time import time as timefunc
from psutil import cpu_percent, virtual_memory

from TelegramBot.config import SUDO_USERID
from TelegramBot import bot, scheduler, loop
from TelegramBot import BotStartTime, SABNZBD_ENDPOINT
from TelegramBot.helpers.functions import get_readable_bytes
from TelegramBot.helpers.pasting_services import katbin_paste
from TelegramBot.helpers.functions import get_readable_time



downloading_status_chatids = {} #saves chatid where downloading status page is active.
postprocess_status_chatids = {} #saves chatid where postprocessing status page is active.


class UsenetBot:

	def __init__(self):
		#Number of blocks in progress bar,
		self.__number_of_blocks = 11

		#progress bar ascii animation
		self.__remaining_block_ascii = "▱"
		self.__completed_block_ascii = "▰"

		self.SABNZBD_API = f"{SABNZBD_ENDPOINT}&output=json"
		self.client =  httpx.AsyncClient()


	def footer_message(self, speed=None):
		botuptime = get_readable_time(timefunc() - BotStartTime)
		total, used, free = disk_usage(".")
		free_space = get_readable_bytes(free)
		total_space = get_readable_bytes(total)
		cpu_usage= f"{cpu_percent()}%"
		ram_usage= f"{virtual_memory().percent}%"

		msg = f"CPU: {cpu_usage} | RAM: {ram_usage}  \n"
		msg += f"Total: {total_space} | Free: {free_space}\n"
		msg += f"UPTIME: {botuptime} | DL-Speed: {speed}\n"
		return msg
	
	async def downloading_status_page(self):
		"""Generate status page for downloading progress message."""
		
		try:
		    downloading_response = await self.client.get(self.SABNZBD_API, params={'mode': 'queue'})
		    downloading_queue_list = downloading_response.json()['queue']['slots']
		except:
			downloading_queue_list = []
		
		try:
		    postprocessing_response = await self.client.get(self.SABNZBD_API, params={'mode': 'history'})
		    postprocessing_queue_list = [slot for slot in postprocessing_response.json()['history']['slots'] if slot['status'] not in ['Completed', 'Failed']]
		except:
			postprocessing_queue_list = []
		
		status_page = ""
		
		if downloading_queue_list:
			status_page += "**Downloading -\n\n**"
			
			for index, queue in enumerate(downloading_queue_list):
			    filled_blocks = round(int(queue['percentage']) * self.__number_of_blocks / 100)
			    unfilled_blocks = self.__number_of_blocks - filled_blocks
			    
			    file_name = queue['filename']
			    if re.search(r"(http|https)", file_name):
			    	file_name = "Adding file from ID."
			    
			    status_page += f"**🗂 FileName:** __{file_name}__\n"
			    status_page += f"**{queue['percentage']}%**  `[{self.__completed_block_ascii * filled_blocks}{self.__remaining_block_ascii * unfilled_blocks}]`\n"
			    status_page += f"**{queue['sizeleft']}** __remaining of__ **{queue['size']}**\n"
			    status_page += f"**Status:** {queue['status']} | **ETA:** {queue['timeleft']}\n"
			    status_page += f"**Task ID:** `{queue['nzo_id']}`\n\n"
			    
			    if index == 4 and len(downloading_queue_list) > 4:
			        status_page += f"➕ {max(len(downloading_queue_list)-4, 0)} Ongoing Task...\n\n"
			        break

		if postprocessing_queue_list:
		    if status_page:
		    	status_page += "━━━━━━━━━━━━━━━━━━━━━\n"
			
		    status_page += "**Post Processing -\n\n**"		    
		    for index, history in enumerate(postprocessing_queue_list):
		        status_page += f"**🗂 FileName :** __{history['name']}__\n"
		        status_page += f"**Status :** __{history['status']}__\n"
		        
		        action = history.get('action_line')
		        if isinstance(action, list) and action_line:
		            status_page += f"**Action :** {action[0]}\n"
		        
		        if action and "Running script:" in action:
		            action = action.replace("Running script:", "")
		            status_page += f"**Action :** __{action.strip()}__\n"
    	    	    
		        if index == 4 and len(postprocessing_queue_list) > 4:
		            status_page += f"➕ Extra Queued Task...\n\n"
		            break
		        status_page += "\n"
		            
		if status_page:
		    status_page += "━━━━━━━━━━━━━━━━━━━━━\n"
		    status_page += self.footer_message()
		return status_page
    
    
	async def postprocessing_status_page(self):
		"""Generate status page for postprocessing progress message."""

		response = await self.client.get(self.SABNZBD_API, params={'mode':'history'})
		response = response.json()
		if not response["history"]["slots"]: return None

		history_list = response["history"]["slots"]

		status_page = ""
		for index, history in enumerate(history_list):
			if history["status"] not in ["Completed", "Failed"]:
				msg = f"**📂 FileName :** __{history['name']}__\n"
				msg += f"**Status :** __{history['status']}__\n"
				action= history.get('action_line', None)
				if isinstance(action, list) and action_line:
					msg += f"**Action:** {action[0]}\n"

				if action:
					if "Running script:" in action:
						action = action.replace("Running script:", "")
					msg += f"**Action :** __{action.strip()}__\n"

				status_page += msg

		if status_page: status_page += self.footer_message()
		return status_page


	async def check_task(self, task_id):
		response = await self.client.get(self.SABNZBD_API, params={'mode':'queue', 'nzo_ids': task_id})
		response = response.json()
		return bool(response["queue"]["slots"])


	async def get_task(self, task_id):
		response = await self.client.get(self.SABNZBD_API, params={'mode':'queue', 'nzo_ids': task_id})
		response = response.json()
		return bool(response["queue"]["slots"])


	async def resume_task(self, task_id):
		isValidTaskID =await self.check_task(task_id)
		if not isValidTaskID: return False

		response = await self.client.get(self.SABNZBD_API, params={'mode':'queue', 'name':'resume', 'value': task_id})
		return response.json()


	async def resumeall_task(self):
		response =await self.client.get(self.SABNZBD_API, params={'mode':'resume'})
		response = response.json()
		return response["status"]


	async def pause_task(self, task_id):
		isValidTaskID = await self.check_task(task_id)
		if not isValidTaskID: return False

		response = await self.client.get(self.SABNZBD_API, params={'mode':'queue', 'name':'pause', 'value': task_id})
		return response.json()

	async def pauseall_task(self):
		response = self.client.get(self.SABNZBD_API, params={'mode':'pause'})
		response = response.json()
		return response["status"]


	async def delete_task(self, task_id):
		isValidTaskID = await self.check_task(task_id)
		if not isValidTaskID: return False

		response = await self.client.get(self.SABNZBD_API, params={'mode':'queue', 'name':'delete', 'value': task_id})
		return response.json()


	async def deleteall_task(self):
		response = await self.client.get(self.SABNZBD_API, params={'mode':'queue', 'name':'delete', 'value':'all'})
		response = response.json()
		return response["status"]


	async def add_nzbfile(self, path_name):
		try:
			async with aiofiles.open(path_name, "rb") as file:
				nzb_content = await file.read()
		except: return False

		payload = {'nzbfile': (path_name.split("/")[-1], nzb_content) }
		params = {'mode':'addfile'}
		response = await self.client.post(self.SABNZBD_API, params=params ,files=payload)
		return response.json()


	async def add_nzburl(self, nzburl):
		params = {'mode':'addurl', "name":nzburl}
		response = await self.client.post(self.SABNZBD_API, params=params)
		return response.json()


	async def clear_progresstask(self, status_message,  chat_id,  progress):
		"""remove job, delete message and clear dictionary of progress bar."""

		scheduler.remove_job(f"{progress}_{str(chat_id)}")
		try: await status_message.delete()
		except: pass #passing errors like status message deleted.

		if progress == "downloading":
			downloading_status_chatids.pop(chat_id)
		elif progress == "postprocessing":
			postprocess_status_chatids.pop(chat_id)


	async def show_downloading_status(self, client, message):
		chat_id = message.chat.id

		# Remove previous status message and scheduled job for that chat_id
		if chat_id in downloading_status_chatids:
			message_id = downloading_status_chatids[chat_id]
			status_message= await client.get_messages(chat_id, message_id)
			await self.clear_progresstask(status_message, chat_id,  progress="downloading")

		# Get the status page
		status_page = await self.downloading_status_page()
		if not status_page:
			return await client.send_message(chat_id, "No ongoing task currently." , reply_to_message_id=message.id)

		# Send the status message and start the job to update the downloading status message after x interval.
		status_message= await client.send_message(chat_id, status_page, reply_to_message_id=message.id)
		downloading_status_chatids[chat_id] = status_message.id

		async def edit_status_message():
			"""Edit the status message  after x seconds."""

			status_page = await self.downloading_status_page()
			if not status_page:
				return await self.clear_progresstask(status_message, chat_id,  progress="downloading")

			try: await status_message.edit(status_page)
			except: await self.clear_progresstask(status_message, chat_id,  progress="downloading")

		scheduler.add_job(edit_status_message, "interval", seconds=10, misfire_grace_time=15,max_instances=2, id=f"downloading_{str(chat_id)}")


	async def show_postprocessing_status(self, client, message):
		chat_id = message.chat.id

		# Remove previous status message and scheduled job for that chat_id
		if chat_id in postprocess_status_chatids:
			message_id = postprocess_status_chatids[chat_id]
			status_message= await client.get_messages(chat_id, message_id)
			await self.clear_progresstask(status_message, chat_id,  progress="postprocessing")

		# Get the status page
		status_page = await self.postprocessing_status_page()
		if not status_page:
			return await client.send_message(chat_id, "No ongoing post processing task found." , reply_to_message_id=message.id)

		# Send the status message and start the job to update the postprocessing status message after x interval.
		status_message= await client.send_message(chat_id, status_page, reply_to_message_id=message.id)
		postprocess_status_chatids[chat_id] = status_message.id

		async def edit_status_message():
			"""Edit the status message  after x seconds."""

			status_page = await self.postprocessing_status_page()
			if not status_page:
				return await self.clear_progresstask(status_message, chat_id,  progress="postprocessing")

			try: await status_message.edit(status_page)
			except Exception as error:
				return await self.clear_progresstask(status_message, chat_id,  progress="postprocessing")

		scheduler.add_job(edit_status_message, "interval", seconds=10, misfire_grace_time=15,max_instances=2, id=f"postprocessing_{str(chat_id)}")
