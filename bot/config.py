import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")

# Subscription prices (in cents)
SUBSCRIPTION_PRICES = {
    'RUB': {
        'month': 29900,  # 299₽
        'quarter': 79900,  # 799₽
        'year': 299900  # 2999₽
    },
    'UAH': {
        'month': 12000,  # 120₴
        'quarter': 32000,  # 320₴
        'year': 120000  # 1200₴
    }
}

SUBSCRIPTION_TITLES = {
    'RUB': {
        'month': 'Подписка на месяц',
        'quarter': 'Подписка на 3 месяца',
        'year': 'Подписка на год'
    },
    'UAH': {
        'month': 'Підписка на місяць',
        'quarter': 'Підписка на 3 місяці',
        'year': 'Підписка на рік'
    }
}

SUBSCRIPTION_DESCRIPTIONS = {
    'RUB': {
        'month': 'Неограниченный доступ к генерации планов питания на 1 месяц',
        'quarter': 'Неограниченный доступ к генерации планов питания на 3 месяца',
        'year': 'Неограниченный доступ к генерации планов питания на 1 год'
    },
    'UAH': {
        'month': 'Необмежений доступ до генерації планів харчування на 1 місяць',
        'quarter': 'Необмежений доступ до генерації планів харчування на 3 місяці',
        'year': 'Необмежений доступ до генерації планів харчування на 1 рік'
    }
}

SUBSCRIPTION_DURATIONS = {
    'month': 30,  # days
    'quarter': 90,  # days
    'year': 365  # days
} 