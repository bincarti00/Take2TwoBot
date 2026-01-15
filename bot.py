from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Our Services", callback_data="services")],
        [InlineKeyboardButton("💰 Payment Methods", callback_data="payments")],
        [InlineKeyboardButton("🧾 Submit TXID", callback_data="txid")],
        [InlineKeyboardButton("🛠 Support", callback_data="support")]
    ]

    await update.message.reply_text(
        "👋 Welcome to *Your Business Name*\n\nSelect an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "services":
        await query.message.reply_text(
            "🛒 *Our Services*\n\n• Service A\n• Service B\n• Service C",
            parse_mode="Markdown"
        )

    elif query.data == "payments":
        await query.message.reply_text(
            "💰 *Crypto Payment Methods*\n\n"
            "BTC:\n`YOUR_BTC_ADDRESS`\n\n"
            "ETH:\n`YOUR_ETH_ADDRESS`\n\n"
            "USDT:\n`YOUR_USDT_ADDRESS`\n\n"
            "After payment, tap *Submit TXID*.",
            parse_mode="Markdown"
        )

    elif query.data == "txid":
        context.user_data["awaiting_txid"] = True
        await query.message.reply_text("🧾 Paste your transaction ID (TXID).")

    elif query.data == "support":
        context.user_data["support"] = True
        await query.message.reply_text("🛠 Send your message below.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_txid"):
        txid = update.message.text

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💰 *New Payment*\n\nUser: @{update.message.from_user.username}\nTXID:\n`{txid}`",
            parse_mode="Markdown"
        )

        await update.message.reply_text(
            "✅ *Payment Confirmed!*\nThank you.",
            parse_mode="Markdown"
        )

        context.user_data.clear()
        return

    if context.user_data.get("support"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🛠 *Support Message*\n\nUser: @{update.message.from_user.username}\nMessage:\n{update.message.text}",
            parse_mode="Markdown"
        )

        await update.message.reply_text("✅ Support received your message.")
        context.user_data.clear()

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
