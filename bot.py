from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# ✅ Replace with your Telegram User IDs
ALLOWED_USERS = [6202472342]  # Add your ID here

# Initialize balances and history
balances = {"monu": 0, "md": 0}
adjustments = {"md_extra_withdrawn": 0}
history = []

# 🔒 Access Control
async def is_authorized(update: Update):
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("🚫 Access Denied: You are not authorized to use this bot.")
        return False
    return True

# Start command
async def start(update: Update, context: CallbackContext):
    if not await is_authorized(update):
        return
    await update.message.reply_text("Welcome to the Profit Maintain Bot! How can I help you today?")

# Add profit command
async def add_profit(update: Update, context: CallbackContext):
    if not await is_authorized(update):
        return
    try:
        profit = int(context.args[0])
        share = profit // 2

        # Update balances
        balances["monu"] += share
        balances["md"] += share

        # Log history
        history.append(f"Profit added: ₹{profit} (₹{share} each)")
        await update.message.reply_text(
            f"Profit of ₹{profit} added.\n"
            f"Each partner's share: ₹{share}\n"
            f"Current Balances:\nMonu: ₹{balances['monu']}\nMD: ₹{balances['md']}"
        )
    except:
        await update.message.reply_text("Error: Use the command like this - /addprofit [amount]")

# Add payment command
async def add_payment(update: Update, context: CallbackContext):
    if not await is_authorized(update):
        return
    try:
        payment = int(context.args[0])

        # Update balances
        balances["monu"] -= payment
        adjustments["md_extra_withdrawn"] += payment

        # Log history
        history.append(f"MD transferred ₹{payment} to Monu.")
        await update.message.reply_text(
            f"MD transferred ₹{payment} to Monu.\n"
            f"Current Balances:\nMonu: ₹{balances['monu']}\n"
            f"MD owes Monu: ₹{adjustments['md_extra_withdrawn']}"
        )
    except:
        await update.message.reply_text("Error: Use the command like this - /addpayment [amount]")

# Calculate balance command
async def calculate_balance(update: Update, context: CallbackContext):
    if not await is_authorized(update):
        return
    adjustment_message = (
        f"MD owes Monu: ₹{adjustments['md_extra_withdrawn']}\n"
        if adjustments["md_extra_withdrawn"] > 0 else "No adjustments pending."
    )
    await update.message.reply_text(
        f"Current Balances:\nMonu: ₹{balances['monu']}\n"
        f"MD: ₹{balances['md']}\n{adjustment_message}"
    )

# Show history command
async def show_history(update: Update, context: CallbackContext):
    if not await is_authorized(update):
        return
    if history:
        await update.message.reply_text("\n".join(history))
    else:
        await update.message.reply_text("No transactions yet.")

# Main function
def main():
    bot_token = "7583172405:AAGDad81jomlRIIDuYmh8TBmQF5s5cAyG70"  # Replace with your actual bot token
    app = Application.builder().token(bot_token).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addprofit", add_profit))
    app.add_handler(CommandHandler("addpayment", add_payment))
    app.add_handler(CommandHandler("calculatebalance", calculate_balance))
    app.add_handler(CommandHandler("history", show_history))

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
