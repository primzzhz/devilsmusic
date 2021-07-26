from pyrogram import Client, filters
from pyrogram.types import Message
import tgcalls
import sira
from config import SUDO_USERS
from cache.admins import set
from helpers.wrappers import errors, admins_only


@Client.on_message(
    filters.command("pause")
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def pause(client: Client, message: Message):
    tgcalls.pytgcalls.pause_stream(message.chat.id)
    await message.reply_text("⏸ Di jeda.")


@Client.on_message(
    filters.command("resume")
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def resume(client: Client, message: Message):
    tgcalls.pytgcalls.resume_stream(message.chat.id)
    await message.reply_text("▶️ Di lanjutkan.")


@Client.on_message(
    filters.command(["dc", "end"])
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def stopm(client: Client, message: Message):
    try:
        sira.clear(message.chat.id)
    except:
        pass

    tgcalls.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_text("⏹ Lagu di stop anak anjing.")


@Client.on_message(
    filters.command(["skip", "next"])
    & filters.group
    & ~ filters.edited
)
@errors
@admins_only
async def skip(client: Client, message: Message):
    chat_id = message.chat.id

    sira.task_done(chat_id)
    await message.reply_text("Bentar")
    if sira.is_empty(chat_id):
        tgcalls.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("nothing in queue")
    else:
        tgcalls.pytgcalls.change_stream(
            chat_id, sira.get(chat_id)["file_path"]
        )

        await message.reply_text("⏩ Lagu di skip anak anjing.")


@Client.on_message(
    filters.command("admincache")
)
@errors
@admins_only
async def admincache(client, message: Message):
    set(message.chat.id, [member.user for member in await message.chat.get_members(filter="administrators")])
    await message.reply_text("❇️ Admin cache refreshed!")

# @Client.on_message(filters.command("restartmusic") & filters.user(SUDO_USERS))
# async def restart(c: Client, m: Message):
#   await m.reply_text("Restarting...")
#   args = [sys.executable, "main.py"]
#   os.execl(sys.executable, *args)

@Client.on_message(
    filters.command("helpmusic")
    & filters.group
    & ~ filters.edited
)
async def helper(client , message:Message):
     await message.reply_text("The commands and there use is explained here-: \n `/deezer` To search the song on deezer and get good quality stream \n `/playm` <your song name> play it on voice chat. \n '/playthis` Reply this in response to a link or any telegram audio file it will be played \n `/skip` to skip current song \n `/stopm or /kill` to stop the streaming of song \n `/pause` to pause the stream \n `/resume` to resume the playback. \n Inline search is also supported.")
