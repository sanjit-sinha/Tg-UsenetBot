postproc.py
from logging.handlers import RotatingFileHandler
import subprocess
import requests
import logging
import shlex
import time
import json
import shutil
import sys
import os


#Takes all the parameters given by sabnzbd such as filename,  filepath etc.
try:
        (scriptname, directory, orgnzbname, jobname, reportnumber, category, group, postprocstatus, url) = sys.argv
except:
        print("No commandline parameters found.")
        sys.exit(1)



#==================================================================================

#log file path of sabnzbd log.
LOGFILE_PATH = ""

#Bot token of Telegram Usenet Bot
BOT_TOKEN = ""
#Chat Id of the group/channel to post Final Gdrive Link.
NOTIFICATION_CHAT_ID = ""

RCLONE_REMOTE_NAME = ""
RCLONE_UPLOAD_DIRECTORY = ""
DRIVE_UPLOAD_DIRECTORY = f"{RCLONE_REMOTE_NAME}:{RCLONE_UPLOAD_DIRECTORY}"

NZB_FILE_DIRECTORY = ""

rclone_command =  f"rclone copy -v --stats=1s --stats-one-line --drive-stop-on-upload-limit --drive-chunk-size=256M --fast-list --transfers=1 --exclude _UNPACK_*/** --exclude _FAILED_*/** --exclude *.rar --exclude *.txt '{NZB_FILE_DIRECTORY}' '{DRIVE_UPLOAD_DIRECTORY}' "

#To show drive link in telegram notification.
SHOW_DRIVE_LINK = True

#==================================================================================



logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
                RotatingFileHandler(LOGFILE_PATH, mode="w+", maxBytes=5000000, backupCount=10),
                logging.StreamHandler()])


def LOGGER(name: str) -> logging.Logger:
        return logging.getLogger(name)


def get_readable_bytes(size: str) -> str:

        dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

        if not size:
                return ""
        power = 2**10
        raised_to_pow = 0

        while size > power:
                size /= power
                raised_to_pow += 1
        return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"


def telegram_notification(message: str):
                data = {"text": message,  "chat_id": NOTIFICATION_CHAT_ID,  "parse_mode":"html"}
                response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=data)

                if response.status_code == 200:
                                sys.exit(0)

                #if response is not successful
                print("Either the bot_token is not valid or the bot is not allowed to send message in provided chat id.")
                sys.exit(1)


def run_command(command):
        with subprocess.Popen(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        shell=True) as proc:

                while True:
                        output = proc.stdout.readline().decode('UTF-8').strip()

                        if output != '':
                                if ":" in output:
                                                output = output.split(":")[-1].strip()
                                LOGGER(__name__).info(f"Uploading to drive: {output}")

                        if output == '' and proc.poll() is not None:
                                LOGGER(__name__).info("File has been successfully uploaded to gdrive.")
                                break

if category == "*": category = "Default"
reasons = {
    "1": "Failed verification",
    "2": "Failed unpack",
    "3": "Failed unpack / verification",
}

if str(postprocstatus) in reasons:
    reason = reasons[postprocstatus]
    notification_message = f"<code>🗂 {jobname}</code>\n\n{reason} "
    telegram_notification(message=notification_message)
    sys.exit(1)


run_command(rclone_command)

#deleting file from local drive.
shutil.rmtree(directory)

try:
        file_size = subprocess.check_output(["rclone",  "size", "--json", f"{DRIVE_UPLOAD_DIRECTORY}/{jobname}"]).decode("utf-8")
        file_size = json.loads(file_size)
        file_size = get_readable_bytes(file_size["bytes"])
except:
        file_size = "N/A"


drive_link = ""
if SHOW_DRIVE_LINK:
        drive_link = subprocess.check_output(["rclone",  "link", f"{DRIVE_UPLOAD_DIRECTORY}/{jobname}"]).decode("utf-8")

        if "drive.google.com" not in drive_link:
                drive_link = "Something went wrong!"

        print(drive_link)
        drive_link = f'<a href="{drive_link}">Drive Link</a>'


notification_message = f"<code>🗂 {jobname}</code>\n\n{file_size} | Success | {category} | {drive_link} "
telegram_notification(message=notification_message)
