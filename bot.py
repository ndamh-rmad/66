import os
import asyncio
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from httpx import AsyncClient

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# قائمة بالسور وأسمائها وأصواتها (بصوت هيثم الدخين)
surahs = [
    {"name": "الفاتحة", "url": "https://server.mp3quran.net/haitham/001.mp3"},
    {"name": "البقرة", "url": "https://server.mp3quran.net/haitham/002.mp3"},
    {"name": "آل عمران", "url": "https://server.mp3quran.net/haitham/003.mp3"},
    # أكمل باقي السور إذا أردت
]

async def send_random_surah(application):
    while True:
        surah = random.choice(surahs)
        try:
            await application.bot.send_audio(
                chat_id=CHANNEL_ID,
                audio=surah["url"],
                caption=f"📖 {surah['name']}\n🎙️ القارئ: هيثم الدخين"
            )
        except Exception as e:
            print("خطأ في الإرسال:", e)
        await asyncio.sleep(300)  # كل 5 دقائق

# أوامر البوت

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في بوت القرآن الكريم 🎧")

async def random_surah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    surah = random.choice(surahs)
    await update.message.reply_audio(
        audio=surah["url"],
        caption=f"📖 {surah['name']}\n🎙️ القارئ: هيثم الدخين"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال!")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # أوامر المستخدم
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_surah))
    app.add_handler(CommandHandler("ping", ping))

    # بدء مهمة إرسال السور كل 5 دقائق
    app.create_task(send_random_surah(app))

    print("🤖 البوت يعمل الآن...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
