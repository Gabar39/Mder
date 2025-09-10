from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

data = {"salary": 0, "expenses": []}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 إضافة راتب", callback_data="add_salary")],
        [InlineKeyboardButton("🧾 إضافة مصروف", callback_data="add_expense")],
        [InlineKeyboardButton("📊 عرض إحصائيات", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("مرحبًا! أنا بوت الإدارة المالية 📑", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "add_salary":
        await query.edit_message_text("أرسل مبلغ الراتب الشهري 💵")
        context.user_data["action"] = "salary"
    elif query.data == "add_expense":
        await query.edit_message_text("أرسل المصروف بهذا الشكل:\n`المبلغ - النوع`")
        context.user_data["action"] = "expense"
    elif query.data == "stats":
        total_expenses = sum(x["amount"] for x in data["expenses"])
        remaining = data["salary"] - total_expenses
        text = f"💵 الراتب: {data['salary']} دينار\n"
        text += f"🧾 المصروفات: {total_expenses} دينار\n"
        text += f"📊 المتبقي: {remaining} دينار"
        await query.edit_message_text(text)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get("action")
    if action == "salary":
        data["salary"] = int(update.message.text)
        await update.message.reply_text("✅ تم تسجيل الراتب.")
    elif action == "expense":
        try:
            amount, category = update.message.text.split("-")
            data["expenses"].append({"amount": int(amount.strip()), "category": category.strip()})
            await update.message.reply_text("✅ تم إضافة المصروف.")
        except:
            await update.message.reply_text("❌ الصيغة غير صحيحة. استخدم: المبلغ - النوع")

def main():
    import os
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()# Mder
