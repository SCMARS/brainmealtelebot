import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Create a model
model = genai.GenerativeModel('gemini-pro')

# Test the API
try:
    response = model.generate_content("Hello, how are you?")
    print("Gemini API Test Response:", response.text)
    print("✅ Gemini API работает корректно")
except Exception as e:
    print("❌ Ошибка Gemini API:", str(e)) 