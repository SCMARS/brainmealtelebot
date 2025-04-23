import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")

# Subscription prices
SUBSCRIPTION_PRICE = 999  # in cents
SUBSCRIPTION_TITLE = "Premium Subscription"
SUBSCRIPTION_DESCRIPTION = "Get unlimited access to meal plan generation" 