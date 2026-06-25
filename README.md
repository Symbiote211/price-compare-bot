# Price Compare Bot

Telegram бот для сравнения цен в магазинах.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте переменные окружения:
```bash
cp .env.example .env
# Заполните TELEGRAM_BOT_TOKEN и GOOGLE_APPLICATION_CREDENTIALS
```

3. Установите Tesseract OCR:
- Скачайте с https://github.com/UB-Mannheim/tesseract/wiki
- Добавьте в PATH

## Запуск

```bash
python bot.py
```

Или двойной клик `run.bat`

## Команды бота

- `/start` — приветствие
- `/help` — помощь
- `/track <название>` — добавить в отслеживание
- `/list` — список отслеживаемых товаров
- Отправь текст — поиск товара
- Отправь фото — распознавание + поиск
