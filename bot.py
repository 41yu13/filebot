import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Setup logging supaya mudah cek error
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Simpan file berdasarkan ID unik (sementara di RAM)
file_storage = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args:
        code = args[0]
        if code in file_storage:
            file_id, file_type = file_storage[code]
            try:
                if file_type == "photo":
                    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_id)
                elif file_type == "video":
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=file_id)
                else:  # document
                    await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
            except Exception as e:
                logger.error(f"Gagal mengirim bahan coli: {e}")
                await update.message.reply_text("Gagal mengirim bahan coli.")
        else:
            await update.message.reply_text("Bahan coli tidak ketemu.")
    else:
        await update.message.reply_text("Kirim bahan coli ke bot ini untuk disimpan.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    file_type = None

    if update.message.document:
        file = update.message.document
        file_type = "document"
    elif update.message.photo:
        file = update.message.photo[-1]  # Ambil foto resolusi tertinggi
        file_type = "photo"
    elif update.message.video:
        file = update.message.video
        file_type = "video"

    if file:
        code = str(file.file_id)[-8:]  # kode unik dari 8 digit terakhir file_id
        file_storage[code] = (file.file_id, file_type)
        await update.message.reply_text(f"Bahan coli sudah disimpan yey!\nLink: t.me/{context.bot.username}?start={code}")
        logger.info(f"bahan coli disimpan dengan kode: {code}")
    else:
        await update.message.reply_text("File tidak dikenali.")

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        logger.error("Token bot tidak ditemukan! Pastikan environment variable BOT_TOKEN sudah diset.")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL | filters.PHOTO, handle_file))

    logger.info("Bot mulai berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
