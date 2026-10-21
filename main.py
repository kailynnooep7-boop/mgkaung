import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# API Keys
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("မင်္ဂလာပါ! ကျွန်တော်က Group မှာ စကားပြောပေးမယ့် AI Bot ဖြစ်ပါတယ်။")

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    
    try:
        prompt = f"You are a friendly group member. Reply nicely in Burmese to this message: {user_text}"
        response = model.generate_content(prompt)
        reply_text = response.text
        
        await update.message.reply_text(reply_text)
    except Exception as e:
        print(f"Error: {e}")

def main():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN is missing!")
        return
        
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    # Render နှင့် Python 3.14 အတွက် အသင့်တော်ဆုံး polling ပုံစံ
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
