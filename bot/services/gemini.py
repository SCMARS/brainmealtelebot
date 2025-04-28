import google.generativeai as genai
from bot.config import GEMINI_API_KEY
import logging
import asyncio

genai.configure(api_key=GEMINI_API_KEY)

class GeminiService:
    @staticmethod
    async def generate_meal_plan(profile: dict, days: int, existing_meals: list = None) -> str:
        """Generate meal plan using Gemini API"""
        try:
            # Validate profile
            required_fields = ['age', 'gender', 'weight', 'height', 'goal']
            missing_fields = [field for field in required_fields if field not in profile]
            if missing_fields:
                return f"❌ Необходимо предоставить полный профиль пользователя. Отсутствуют поля: {', '.join(missing_fields)}"

            # Create model for each request
            model = genai.GenerativeModel ('gemini-1.5-flash')
            
            # Format existing meals info
            existing_meals_info = ""
            if existing_meals and len(existing_meals) > 0:
                existing_meals_info = "\nСуществующие приемы пищи:\n"
                for meal in existing_meals:
                    existing_meals_info += f"- {meal['type']}: {meal['name']} ({meal['calories']} ккал, {meal['protein']}г белка, {meal['carbs']}г углеводов, {meal['fat']}г жиров)\n"

            # Convert gender to readable format
            gender_display = "мужской" if profile['gender'] == 'male' else "женский"

            prompt = f"""Создай детальный план питания на {days} {'день' if days == 1 else 'дня'} для человека со следующими параметрами:
- Возраст: {profile['age']} лет
- Пол: {gender_display}
- Вес: {profile['weight']} кг
- Рост: {profile['height']} см
- Цель: {profile['goal']}
- Калории в день: {profile.get('calories', 2000)}
- Предпочтения в еде: {profile.get('food_preferences', 'нет ограничений')}
- Аллергии: {profile.get('allergies', 'нет')}
- Уровень активности: {profile.get('activity_level', 'умеренный')}{existing_meals_info}

План должен включать:
1. Расписание приемов пищи (завтрак, обед, ужин, перекусы)
2. Для каждого приема пищи:
   - Название блюда
   - Ингредиенты и их количество
   - Калории
   - Белки, жиры, углеводы
   - Время приема
3. Общую статистику по дням
4. Рекомендации по приготовлению

ВАЖНО: 
1. Ответ должен быть в формате текста, удобном для чтения в Telegram
2. Используй эмодзи для лучшей читаемости
3. Разделяй приемы пищи и дни четкими заголовками
4. Добавляй статистику в конце каждого дня
5. В конце добавь общие рекомендации по приготовлению

Пример формата:
🍽️ ДЕНЬ 1

🍳 ЗАВТРАК (08:00)
• Овсяная каша с фруктами
• Калории: 350 ккал
• БЖУ: 12г белков, 60г углеводов, 8г жиров
• Ингредиенты: овсянка, молоко, банан, мед

🍲 ОБЕД (13:00)
• Куриная грудка с рисом
• Калории: 450 ккал
• БЖУ: 35г белков, 50г углеводов, 10г жиров
• Ингредиенты: куриная грудка, рис, овощи

📊 СТАТИСТИКА ЗА ДЕНЬ:
• Калории: 2000 ккал
• Белки: 120г
• Углеводы: 200г
• Жиры: 50г

👨‍🍳 РЕКОМЕНДАЦИИ:
• Рекомендации по приготовлению..."""
            
            logging.info(f"Generating meal plan with prompt: {prompt}")
            
            # Use asyncio for async call
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))
            
            if not response or not response.text:
                logging.error("Empty response from Gemini API")
                return "❌ Извините, произошла ошибка при генерации плана питания. Пожалуйста, попробуйте позже."
            
            return response.text
            
        except Exception as e:
            logging.error(f"Error generating meal plan: {str(e)}")
            return "❌ Извините, произошла ошибка при генерации плана питания. Пожалуйста, попробуйте позже." 