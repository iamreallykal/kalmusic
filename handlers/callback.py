

from time import time
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from helpers.decorators import authorized_users_only
from config import ALIVE_EMOJI as alv
from config import BOT_NAME as bn, BOT_IMG, BOT_USERNAME, OWNER_NAME, GROUP_SUPPORT, UPDATES_CHANNEL, ASSISTANT_NAME, UPSTREAM_REPO
from handlers.play import cb_admin_check


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>β¨ Welcome [{query.message.chat.first_name}](tg://user?id={query.message.chat.id})!</b>

**π­ [{bn}](https://t.me/{GROUP_SUPPORT}) allows you to play music on groups through the new Telegram's voice chats!**

π‘ Find out all the **Bot's commands** and how they work by clicking on the **Β» π Commands** button!""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "β Add me to your group β", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "π Commandββ", callback_data="cbhelp"
                    ),
                    InlineKeyboardButton(
                        "β€οΈ Donate", url=f"https://t.me/{OWNER_NAME}")
                ],[
                    InlineKeyboardButton(
                        "π₯ Official Groupββ", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "π£ Official Channel", url=f"https://t.me/{UPDATES_CHANNEL}")
                ],[
                    InlineKeyboardButton(
                        "π Source Code", url=f"{UPSTREAM_REPO}")
                ],[
                    InlineKeyboardButton(
                        "β About meββ", callback_data="cbabout"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbabout"))
async def cbabout(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>β **About  [{bn}](https://t.me/{BOT_USERNAME})**</b> 

β  **A powerfull bot for playing music for groups!

β  Working with pyrogram

β  Using Python 3.9.7

β  Can play and download music or videos from YouTube

β  I can make you happy

β  For more info click /help

__{bn} licensed under the GNU General Public License v.3.0__

β’ Updates channel @{UPDATES_CHANNEL}
β’ Group Support @{GROUP_SUPPORT}
β’ Assistant @{ASSISTANT_NAME}
β’ Here is my [Owner](https://t.me/{OWNER_NAME})**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Backβ", callback_data="cbstart"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} Here is the help menu !</b>

**In this menu you can open several available command menus, in each command menu there is also a brief explanation of each command**

π‘ Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Basic Cmd", callback_data="cbbasic"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "π Admin Cmd", callback_data="cbadmin"
                    ),
                    InlineKeyboardButton(
                        "π Sudo Cmd", callback_data="cbsudo"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "π Fun Cmd", callback_data="cbfun"),
                    InlineKeyboardButton(
                        "π Ownertools", callback_data="cbowner"
                    ) 
                ],
                [
                    InlineKeyboardButton(
                        "π Back", callback_data="cbstart"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} basic commands for bots

[GROUP SETTINGS]
/play (title) - play music via youtube
/ytp (title) - play music live
/stream (reply to audio) - play music via reply to audio
/playlist - view queue list
/song (title) - download music from youtube
/search (title) - search for music from youtube in detail
/saavn (title) - download music from saavn
/video (title) - download music from youtube in detail
/lyric (title) - search for lyrics
/shazam (reply audio) - for identifying song name
/q (reply text) - to make a quotes sticker
/id - to show your id or chat id
[ MORE ]
/alive - check alive bot
/start - starting bot

π‘ Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} command for group admin

/player - view playback status
/pause - pauses playing music
/resume - resume paused music
/skip - skip to next song
/end - mute the music
/userbotjoin - invite assistant to join the group
/musicplayer (on / off) - turn on / off the music player in your group

π‘ Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""π€΄ **here is the owner commands**

/stats - show the bot statistic
/broadcast (reply to message) - send a broadcast message from bot
/block (user id - duration - reason) - block user for using your bot
/unblock (user id - reason) - unblock user you blocked for using your bot
/blocklist - show you the list of user was blocked for using your bot

π note: all commands owned by this bot can be executed by the owner of the bot without any exceptions.

π‘ Bot by @{OWNER_NAME}""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("π Go Back", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **command for sudo**

**/userbotleaveall - remove assistant from all groups
/gcast - send global messages via assistant
/rmd - delete downloaded files
/uptime - for see the uptime and start time bot launched
/sysinfo - to see system bot info
/eval and /sh - running evaluator or shell
if using heroku
/usage - for check you dyno heroku
/update - for build update your bot
/restart - restart/reboot your bot
/setvar (var) (value) - to update your value variable on heroku
/delvar (var) - to delete your var on heroku.

π‘ Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbfun"))
async def cbfun(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b>{alv} **Command fun**

**/chika - check it yourself
/wibu - check it yourself
/asupan - check yourself
/truth - check yourself
/dare - check it yourself
/q - to make quotes text
/paste - pasting your text or document to pastebin into photo

π‘ Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Back", callback_data="cbhelp"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**HOW TO USE THIS BOTT :**

**1.) First, add to your group.
2.) Then make admin with all permissions except anonymous admin.
3.) Add @{ASSISTANT_NAME} to your group or type `/userbotjoin` to invite assistant.
4.) Turn on voice chat first before playing music.

π‘ Bot by @{OWNER_NAME}**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π Close", callback_data="close"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbhplay"))
async def cbhplay(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""How to play music on {bn} {alv}

β’ `/play (query)` - for playing music via youtube
β’ `/ytp (query)` - play music directly from youtube

π Updates channel [Click here](https://t.me/{UPDATES_CHANNEL})""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("π Back", callback_data="cbplayback"),
                ],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbplayback"))
async def cbplayback(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**π Hey !! Give me something to play and searching on youtube.**""", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("Group Support", url=f"https://t.me/{GROUP_SUPPORT}"),
                ],
                [
                   InlineKeyboardButton("See Command", callback_data="cbhplay"),
                ],
                [
                   InlineKeyboardButton("ποΈ Close", callback_data="closed"),
                ],
            ]
        ),
    )
