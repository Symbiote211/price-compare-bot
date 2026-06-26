import asyncio
import tempfile
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
import search
import categories
import image_recognizer
from ocr import extract_text_from_image
from database import Database

db = Database()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот для сравнения цен.\n\n"
        "Отправь мне:\n"
        "📝 Название товара — и я найду цены\n"
        "📷 Фото товара — и я распознаю его\n\n"
        "Команды:\n"
        "/track <название> — добавить в отслеживание\n"
        "/list — мои отслеживаемые товары\n"
        "/categories — категории товаров\n"
        "/help — помощь"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Как пользоваться:\n\n"
        "1. Отправь название товара (например: 'Dove гель для душа')\n"
        "2. Или отправь фото товара\n"
        "3. Я покажу цены в разных магазинах\n\n"
        "📊 Отслеживание цен:\n"
        "/track <название> — добавить товар\n"
        "/list — список отслеживаемых\n\n"
        "📂 Категории:\n"
        "/categories — список категорий\n"
        "/category <название> — поиск в категории"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    if not query:
        return

    await update.message.reply_text("Ищу цены...")

    try:
        results = await asyncio.to_thread(search.search_all_stores, query)
        response = search.format_results(results)
        await update.message.reply_text(response)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Search error: {e}")
        await update.message.reply_text("Ошибка поиска: " + str(e)[:100])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        image_path = tmp.name
        try:
            data = await file.download_as_bytearray()
            tmp.write(data)
        except Exception:
            pass

    try:
        text = extract_text_from_image(image_path)
        if not text:
            text = image_recognizer.recognize_product(image_path)

        if text:
            results = search.search_all_stores(text)
            response = search.format_results(results)
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("❌ Не удалось распознать товар на фото")
    finally:
        if os.path.exists(image_path):
            os.unlink(image_path)

async def track_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /track <название товара>")
        return

    product_name = " ".join(context.args)
    user_id = update.message.from_user.id

    await db.connect()
    await db.add_tracked_product(user_id, product_name)
    await db.close()

    await update.message.reply_text(f"✅ Добавлено в отслеживание: {product_name}")

async def list_tracked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    await db.connect()
    products = await db.get_tracked_products(user_id)
    await db.close()

    if not products:
        await update.message.reply_text("📭 У вас нет отслеживаемых товаров")
        return

    lines = ["📋 Ваши отслеживаемые товары:\n"]
    for p in products:
        lines.append(f"• {p['product_name']}")

    await update.message.reply_text("\n".join(lines))

async def list_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = ["📂 Категории товаров:\n"]
    for key, cat in categories.CATEGORIES.items():
        lines.append(f"{cat['emoji']} {cat['name']}")
    lines.append("\nИспользуйте /category <название> для поиска в категории")
    await update.message.reply_text("\n".join(lines))

async def category_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Использование: /category <название категории>\n\nКатегории: шампуни, кремы, гели, дезодоранты, парфюмерия, макияж")
        return

    category_name = " ".join(context.args).lower()

    category_key = None
    for key, cat in categories.CATEGORIES.items():
        if category_name in cat["name"].lower() or category_name in cat["keywords"]:
            category_key = key
            break

    if not category_key:
        await update.message.reply_text("❌ Категория не найдена. Используйте /categories для списка категорий")
        return

    cat = categories.CATEGORIES[category_key]
    query = cat["keywords"][0]

    await update.message.reply_text(f"🔍 Ищу {cat['name']} ({cat['emoji']})...")

    try:
        results = await asyncio.to_thread(search.search_all_stores, query)
        response = search.format_results(results)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Ошибка поиска: {str(e)[:100]}")

def main():
    from config import PROXY_URL
    
    token = TELEGRAM_BOT_TOKEN or "8887194195:AAFJImdIJ0zYloZijOkgax08EB9KQcd_G5Y"
    builder = Application.builder().token(token)
    
    if PROXY_URL:
        from telegram.request import HTTPXRequest
        request = HTTPXRequest(proxy=PROXY_URL)
        builder = builder.request(request)
    
    application = builder.build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("track", track_product))
    application.add_handler(CommandHandler("list", list_tracked))
    application.add_handler(CommandHandler("categories", list_categories))
    application.add_handler(CommandHandler("category", category_search))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("Bot started!")
    application.run_polling()

if __name__ == "__main__":
    main()
