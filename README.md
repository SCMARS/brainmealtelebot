# BrainMeal Telegram Bot

Telegram бот для генерации персональных планов питания с использованием AI.

## Функциональность

- Сбор и хранение профиля пользователя (возраст, вес, рост, цели)
- Генерация планов питания на день и неделю
- Система подписок с оплатой через Telegram Payments
- Ограничение бесплатных генераций (1 раз в день)
- Неограниченный доступ для подписчиков

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SCMARS/brainmealtelebot.git
cd brainmealtelebot
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example` и заполните необходимые переменные:
```bash
cp .env.example .env
```

## Настройка

1. Получите токен бота у [@BotFather](https://t.me/BotFather)
2. Получите API ключ Gemini на [Google AI Studio](https://makersuite.google.com/app/apikey)
3. Заполните файл `.env` полученными данными

## Запуск

1. Активируйте виртуальное окружение (если еще не активировано):
```bash
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

2. Запустите бота:
```bash
python -m bot.main
```

## Управление ботом

Используйте скрипт `manage.py` для управления ботом:

```bash
python manage.py start    # Запустить бота
python manage.py stop     # Остановить бота
python manage.py restart  # Перезапустить бота
python manage.py status   # Показать статус
python manage.py logs     # Показать логи
```

## База данных

Бот использует SQLite для хранения данных. База данных автоматически создается при первом запуске в файле `bot.db`.

## Команды бота

- `/start` - Начать работу с ботом
- `/profile` - Создать или обновить профиль
- `/generateforday` - Сгенерировать план питания на день
- `/generateforweek` - Сгенерировать план питания на неделю (требуется подписка)
- `/subscribe` - Оформить подписку
- `/analytics` - Просмотр базовой аналитики
- `/detailed_analytics` - Просмотр детальной аналитики
- `/help` - Показать справку

## Структура проекта

```
brainmealtelebot/
├── bot/
│   ├── handlers/      # Обработчики команд
│   ├── keyboards/     # Клавиатуры
│   ├── services/      # Сервисы (AI, база данных)
│   └── main.py        # Точка входа
├── .env              # Конфигурация
├── .env.example      # Пример конфигурации
├── manage.py         # Скрипт управления
└── requirements.txt  # Зависимости
```

## Лицензия

MIT 