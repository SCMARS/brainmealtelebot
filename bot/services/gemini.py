import google.generativeai as genai
from bot.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class GeminiService:
    @staticmethod
    async def generate_meal_plan(profile: dict, days: int) -> str:
        """Generate meal plan using Gemini API"""
        prompt = f"""Ты — опытный диетолог. Составь план питания на {days} {'день' if days == 1 else 'дня'} для {'мужчины' if profile.get('gender') == 'male' else 'женщины'} {profile.get('age')} лет, {profile.get('weight')} кг, {profile.get('height')} см. Цель — {profile.get('goal')}. {profile.get('dietary_restrictions')}. Укажи завтрак, обед, ужин, перекус. Примерно {profile.get('calories', 2000)} калорий в день. Формат Markdown."""
        
        try:
            response = await model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating meal plan: {str(e)}" 