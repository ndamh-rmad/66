import os
import random
import asyncio
import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # مثال: "@your_channel" أو ID رقمي

API_URL = "https://api.quran.com:443/v4/chapters"

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك في بوت القرآن الكريم 🎧.\nاكتب /random للحصول على سورة عشوائية.")

# أمر البينق
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("البوت يعمل ✅")

# جلب سورة عشوائية من API
async def get_random_surah():
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        data = response.json()
        chapters = data.get("chapters", [])
        if chapters:
            return random.choice(chapters)
    return None

# إرسال سورة عشوائية
async def random_surah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    surah = await get_random_surah()
    if surah:
        name = surah["name_arabic"]
        translated = surah["name_simple"]
        number = surah["id"]
        message = f"📖 سورة {name} ({translated}) - رقم {number}"
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("تعذر جلب سورة حالياً، حاول لاحقاً.")

# إرسال تلقائي كل 6 ساعات
async def send_random_surah(app):
    while True:
        surah = await get_random_surah()
        if surah:
            name = surah["name_arabic"]
            translated = surah["name_simple"]
            number = surah["id"]
            message = f"📖 سورة {name} ({translated}) - رقم {number}"
            await app.bot.send_message(chat_id=CHANNEL_ID, text=message)
        await asyncio.sleep(6 * 60 * 60)  # كل 6 ساعات

# نقطة البداية
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("random", random_surah))
    app.add_handler(CommandHandler("ping", ping))

    # إرسال تلقائي بالخلفية
    app.create_task(send_random_surah(app))

    print("✅ البوت يعمل الآن...")
    await app.run_polling()

# تشغيل
if __name__ == "__main__":
    asyncio.run(main())
