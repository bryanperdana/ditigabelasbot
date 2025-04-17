import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# OpenAI API Key & Telegram Token
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

character_prompt = (
    "Kamu adalah seorang analis makroekonomi dan crypto enthusiast. "
    "Jawabanmu profesional tapi engaging, dan kamu juga bisa bantu buat gambar atau kode jika diminta."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku bisa bantu jawab soal ekonomi, kripto, atau bikin gambar AI. Coba tanya aku!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    if "gambar" in user_input.lower():
        try:
            image_response = client.images.generate(
                prompt=user_input,
                n=1,
                size="512x512"
            )
            image_url = image_response.data[0].url
            await update.message.reply_photo(photo=image_url)
        except Exception as e:
            await update.message.reply_text(f"❌ Gagal buat gambar: {e}")
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=[
                    {"role": "system", "content": character_prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response.choices[0].message.content
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text(f"❌ Gagal menjawab: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
