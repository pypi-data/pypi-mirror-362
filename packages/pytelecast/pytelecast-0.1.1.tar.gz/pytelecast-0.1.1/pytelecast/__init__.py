# pyte/__init__.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from .core import broadcast_message
from .db_json import add_user, get_all_users as json_get
from .db_sqlite import add_user as sql_add, get_all_users as sql_get

def init_broadcast(app, sudo_users: list[int], db_type="json", db_url=None):
    assert db_type in ["json", "sqlite", "mongo"], "Invalid db_type"

    # Set DB
    if db_type == "mongo":
        from .db_mongo import setup_mongo
        if not db_url:
            raise ValueError("MongoDB selected but db_url not provided.")
        add_user_fn, get_users_fn = setup_mongo(db_url)
        print("📦 Using MongoDB as DB backend.")
    elif db_type == "sqlite":
        add_user_fn = sql_add
        get_users_fn = sql_get
        print("📦 Using SQLite as DB backend.")
    else:
        add_user_fn = json_get.__globals__["add_user"]
        get_users_fn = json_get
        print("📦 Using JSON as DB backend.")

    print(f"👑 Sudo Users Set: {sudo_users}")
    print("✅ Broadcast module initialized successfully.")
  
    # Auto collect users
    async def collect_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
        add_user_fn(update.effective_user.id)

    # /broadcast reply handler
    async def broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in sudo_users:
            return
        if not update.message.reply_to_message:
            return await update.message.reply_text("❗ Reply to a message to broadcast.")

        context.user_data["broadcast_msg"] = update.message.reply_to_message

        buttons = [
            [InlineKeyboardButton("✅ Confirm", callback_data="confirm_broadcast")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_broadcast")]
        ]

        msg = update.message.reply_to_message
        if msg.text:
            await update.message.reply_text(msg.text_html, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
        elif msg.caption and msg.photo:
            await update.message.reply_photo(msg.photo[-1].file_id, caption=msg.caption_html, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))
        elif msg.caption and msg.video:
            await update.message.reply_video(msg.video.file_id, caption=msg.caption_html, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))

    # Confirm or Cancel
    async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if update.effective_user.id not in sudo_users:
            return await query.message.reply_text("❌ Unauthorized")

        if query.data == "cancel_broadcast":
            try:
                await query.message.delete()
            except:
                pass
            await context.bot.send_message(chat_id=update.effective_user.id, text="❌ Broadcast cancelled.")
            context.user_data.pop("broadcast_msg", None)
            return

        msg = context.user_data.get("broadcast_msg")
        if not msg:
            return await context.bot.send_message(chat_id=update.effective_user.id, text="⚠️ No message to broadcast.")

        try:
            await query.message.delete()
        except:
            pass

        user_ids = get_users_fn()
        total, success, blocked, deleted, failed = await broadcast_message(context.bot, user_ids, msg)

        report = (
            "<b>✅ Broadcast Completed</b>\n"
            f"◇ Total Users: {total}\n"
            f"◇ Successful: {success}\n"
            f"◇ Blocked: {blocked}\n"
            f"◇ Deleted: {deleted}\n"
            f"◇ Failed: {failed}"
        )
        await context.bot.send_message(chat_id=update.effective_user.id, text=report, parse_mode="HTML")

    # Register handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, collect_users))
    app.add_handler(MessageHandler(filters.COMMAND & filters.REPLY & filters.Regex("^/broadcast$"), broadcast_cmd))
    app.add_handler(CallbackQueryHandler(confirm_broadcast, pattern="confirm_broadcast|cancel_broadcast"))