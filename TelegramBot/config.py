import json
from os import getenv
from dotenv import load_dotenv
load_dotenv("config.env")

#TelegramBot configs
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
SUDO_USERID = json.loads(getenv("SUDO_USERID"))
AUTHORIZED_CHATS = json.loads(getenv("AUTHORIZED_CHATS"))

#SABnzbd Configs.
SAB_IP= getenv("SAB_IP")
SAB_PORT= getenv("SAB_PORT")
SAB_API_KEY= getenv("SAB_API_KEY")

#NZBHydra Configs.
HYDRA_IP= getenv("HYDRA_IP")
HYDRA_PORT= getenv("HYDRA_PORT")
HYDRA_API_KEY= getenv("HYDRA_API_KEY")
