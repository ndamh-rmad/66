import os
import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue

BOT_TOKEN = os.environ.get("BOT_TOKEN")

surahs = {
    "الفاتحة": "https://archive.org/download/quran-mp3-haitham/001.mp3",
    "البقرة": "https://archive.org/download/quran-mp3-haitham/002.mp3",
    "آل عمران": "https://archive.org/download/quran-mp3-haitham/003.mp3",
    "النساء": "https://archive.org/download/quran-mp3-haitham/004.mp3"
    # يمكنك إضافة المزيد من السور هنا
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في بوت القرآن الكريم 🎧
اكتب /random لإرسال سورة الآن.
اكتب /ping للتأكد أن البوت شغال.")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال")

async def random_surah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name, url = random.choice(list(surahs.items()))
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=url, caption=f"📖 {name} - هيثم الدخين")

async def send_periodic_surah(context: ContextTypes.DEFAULT_TYPE):
    chat_id = os.environ.get("CHAT_ID")
    if chat_id:
        name, url = random.choice(list(surahs.items()))
        await context.bot.send_audio(chat_id=int(chat_id), audio=url, caption=f"📖 {name} - هيثم الدخين")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("random", random_surah))

    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(send_periodic_surah, interval=300, first=10)  # كل 5 دقائق

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
