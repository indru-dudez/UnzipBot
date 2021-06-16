import os
import shutil
import time
import zipfile
import rarfile
from datetime import datetime
from pyrogram.errors import FloodWait
from UnzipBot.functions import absolute_paths
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from Data import Data


# On Files
@Client.on_message(filters.command(["unzip", "unzip@SINNER_UP_bot"]))
async def unzip_files(unzipbot, msg):
    start = datetime.now()
    file_name = msg.reply_to_message.document.file_name
    file_size = msg.reply_to_message.document.file_size
    if file_size > 1524288000:
        await msg.reply("Files with size more than 500 MB aren't allowed.", quote=True)
        return
    try:
        main = await msg.reply("Downloading...", quote=True)
        file = await msg.reply_to_message.download()
        await main.edit("Extracting Files...")
        if file_name.endswith(".zip"):
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall("downloads")
            dir_name = file.replace(".zip", "")
        if file_name.endswith(".rar"):
            with rarfile.RarFile(file, 'r') as rar_ref:
                rar_ref.extractall("downloads")
            dir_name = file.replace(".rar", "")
        extracted_files = [i async for i in absolute_paths(dir_name)]
        for file in extracted_files:
            try:
                await msg.reply_document(file, quote=False, disable_notification=True)
            except FloodWait as e:
                time.sleep(e.x)
        stop = datetime.now()
        await msg.reply(
            f"Extraction Done Successfully..! \n\nTook {round((stop - start).total_seconds() / 60, 2)} minutes.")
    except rarfile.RarCannotExec:
        await msg.reply("**ERROR :** This File is possibly bugged. Cannot extract content. \n\n"
                        "This may happen when a file's extension is manually changed to `.zip`/`.rar` even when file isn't in that format. \n\n"
                        "Try with some other file please.", quote=True
                        )
    except Exception as e:
        await unzipbot.send_message(msg.chat.id, "**ERROR : **" + str(
            e) + "\n\nForward this message to @MysteryBots too solve this problem.", quote=True)
    finally:
        if os.path.isdir("downloads"):
            shutil.rmtree("downloads")
