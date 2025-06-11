from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Simpan file berdasarkan ID unik
file_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        code = args[0]
        if code in file_storage:
            file_id, file_type = file_storage[code]
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
        else:
            await update.message.reply_text("File tidak ditemukan.")
    else:
        await update.message.reply_text("Kirim file ke bot ini untuk disimpan.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    file_type = None

    if update.message.document:
        file = update.message.document
        file_type = "document"
    elif update.message.photo:
        file = update.message.photo[-1]
        file_type = "photo"
    elif update.message.video:
        file = update.message.video
        file_type = "video"

    if file:
        code = str(file.file_id)[-8:]
        file_storage[code] = (file.file_id, file_type)
        await update.message.reply_text(f"File disimpan!\nLink: t.me/{context.bot.username}?start={code}")
    else:
        await update.message.reply_text("File tidak dikenali.")

import os
app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL | filters.PHOTO, handle_file))

app.run_polling()
