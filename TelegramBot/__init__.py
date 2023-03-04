import sys
import time
from asyncio import get_event_loop, new_event_loop, set_event_loop
import uvloop 
import requests

from pyrogram import Client
from TelegramBot.config import *
from TelegramBot.logging import LOGGER
from apscheduler.schedulers.asyncio import AsyncIOScheduler

uvloop.install()
LOGGER(__name__).info("Starting TelegramBot....")
BotStartTime = time.time()


#Checking Python version.
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGER(__name__).critical("""
=============================================================
You MUST need to be on python 3.7 or above, shutting down the bot...
=============================================================
""")
    sys.exit(1)

	
LOGGER(__name__).info("setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

	
LOGGER(__name__).info(
    r"""
____________________________________________________________________
|  _______   _                                ____        _        |
| |__   __| | |                              |  _ \      | |       |
|    | | ___| | ___  __ _ _ __ __ _ _ __ ___ | |_) | ___ | |_      |
|    | |/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \|  _ < / _ \| __|     |
|    | |  __/ |  __/ (_| | | | (_| | | | | | | |_) | (_) | |_      |
|    |_|\___|_|\___|\__, |_|  \__,_|_| |_| |_|____/ \___/ \__|     |
|                    __/ |                                         |
|__________________________________________________________________|   
""")


#Checking Sabnzbd configs.
LOGGER(__name__).info("Checking SABnzbd configs....")
SABNZBD_ENDPOINT = f"http://{SAB_IP}:{SAB_PORT}/sabnzbd/api?apikey={SAB_API_KEY}"
try:
	response = requests.get(SABNZBD_ENDPOINT, timeout=3)
	response.raise_for_status() 
except:
	LOGGER(__name__).critical("Can not establish a successful connection with SABnzbd. Please double-check your configs and try again later.")
	sys.exit(1)
	

#Checking NZBHydra configs.
LOGGER(__name__).info("Checking NZBHydra configs....")	
NZBHYDRA_ENDPOINT = f"http://{HYDRA_IP}:{HYDRA_PORT}/api?apikey={HYDRA_API_KEY}"
NZBHYDRA_URL_ENDPOINT = f"http://{HYDRA_IP}:{HYDRA_PORT}/getnzb/api/replace_id?apikey={HYDRA_API_KEY}"	
NZBHYDRA_STATS_ENDPOINT = f"http://{HYDRA_IP}:{HYDRA_PORT}/api/stats?apikey={HYDRA_API_KEY}"
try:
	response = requests.get(NZBHYDRA_ENDPOINT, timeout=10)
	response.raise_for_status()
	if "Wrong api key" in response.text:
		raise ValueError("Wrong API value in configs.")				
except Exception as error:
	print(error)
	LOGGER(__name__).critical("Can not establish a successful connection with NZBHydra. Please double-check your configs and try again later.")
	sys.exit(1)
	
	
#Starting Apscheduler 
LOGGER(__name__).info("Starting Apscheduler...")
scheduler = AsyncIOScheduler()
scheduler.start()


#starting the client
LOGGER(__name__).info("initiating the client....")
plugins = dict(root="TelegramBot/plugins")       
bot = Client(
    "UsenetBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=plugins)
