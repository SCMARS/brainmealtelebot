import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_payment_token():
    bot_token = os.getenv('BOT_TOKEN')
    payment_token = os.getenv('PAYMENT_TOKEN')
    
    if payment_token == 'your_telegram_payment_token':
        print("❌ Токен платежей не настроен")
        return
    
    try:
        # Test payment token
        response = requests.get(
            f'https://api.telegram.org/bot{bot_token}/getInvoice',
            params={'invoice_id': 'test'}
        )
        print("✅ Токен платежей настроен")
    except Exception as e:
        print("❌ Ошибка проверки платежей:", str(e))

test_payment_token() 