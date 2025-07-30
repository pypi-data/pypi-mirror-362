# pytelecast/core.py

import asyncio
from telegram import Message, Bot, InlineKeyboardMarkup
from telegram.error import Forbidden, BadRequest, TelegramError

async def broadcast_message(bot: Bot, user_ids: list[int], msg: Message):
    total = len(user_ids)
    success = blocked = deleted = failed = 0

    tasks = [send(bot, uid, msg) for uid in user_ids]
    results = await asyncio.gather(*tasks)

    for r in results:
        if r == "success": success += 1
        elif r == "blocked": blocked += 1
        elif r == "deleted": deleted += 1
        else: failed += 1

    return total, success, blocked, deleted, failed

async def send(bot: Bot, user_id: int, msg: Message) -> str:
    try:
        reply_markup = msg.reply_markup if isinstance(msg.reply_markup, InlineKeyboardMarkup) else None

        if msg.photo:
            await bot.send_photo(user_id, msg.photo[-1].file_id, caption=msg.caption_html, parse_mode="HTML", reply_markup=reply_markup)
        elif msg.video:
            await bot.send_video(user_id, msg.video.file_id, caption=msg.caption_html, parse_mode="HTML", reply_markup=reply_markup)
        elif msg.text:
            await bot.send_message(user_id, msg.text_html, parse_mode="HTML", reply_markup=reply_markup)
        else:
            return "failed"
        return "success"

    except Forbidden:
        return "blocked"
    except BadRequest as e:
        return "deleted" if "chat not found" in str(e).lower() else "failed"
    except TelegramError:
        return "failed"