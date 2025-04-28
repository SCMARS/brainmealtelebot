from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.database import DatabaseService
from datetime import datetime, timedelta
import logging

router = Router()
db = DatabaseService()

# Словари для преобразования технических значений в читаемые
GOAL_MAP = {
    'lose_weight': 'Похудение',
    'gain_muscle': 'Набор массы',
    'maintain': 'Поддержание'
}

PLAN_TYPE_MAP = {
    'daily': 'Дневной план',
    'weekly': 'Недельный план'
}

@router.message(Command("analytics"))
async def cmd_analytics(message: Message):
    """Show basic analytics"""
    logging.info(f"Received /analytics command from user {message.from_user.id}")
    try:
        user_id = message.from_user.id
        
        # Get user profile
        profile = db.get_profile(user_id)
        if not profile:
            await message.answer(
                "❌ У вас еще нет профиля. Пожалуйста, создайте его с помощью команды /profile"
            )
            return
        
        # Get subscription status
        is_subscribed = db.get_subscription_status(user_id)
        
        # Get generation history
        history = db.get_generation_history(user_id)
        total_generations = len(history)
        last_week_generations = len([h for h in history if datetime.fromtimestamp(h['timestamp']) > datetime.now() - timedelta(days=7)])
        
        # Count plan types
        plan_types = {}
        for h in history:
            plan_type = PLAN_TYPE_MAP.get(h['plan_type'], h['plan_type'])
            plan_types[plan_type] = plan_types.get(plan_type, 0) + 1
        
        # Create analytics message
        analytics = (
            "📊 *ВАША АНАЛИТИКА:*\n\n"
            f"👤 *Профиль:*\n"
            f"• Возраст: *{profile['age']} лет*\n"
            f"• Вес: *{profile['weight']} кг*\n"
            f"• Рост: *{profile['height']} см*\n"
            f"• Цель: *{GOAL_MAP.get(profile['goal'], profile['goal'])}*\n\n"
            f"🌟 *Статус подписки:* {'Активна' if is_subscribed else 'Неактивна'}\n\n"
            f"📈 *Статистика генераций:*\n"
            f"• Всего сгенерировано: *{total_generations}*\n"
            f"• За последнюю неделю: *{last_week_generations}*\n\n"
            f"📊 *Распределение по типам планов:*\n"
        )
        
        for plan_type, count in plan_types.items():
            analytics += f"• {plan_type}: *{count}*\n"
        
        analytics += "\nИспользуйте /detailed_analytics для просмотра детальной статистики."
        
        await message.answer(analytics, parse_mode="Markdown")
        logging.info(f"Successfully sent analytics to user {user_id}")
    except Exception as e:
        logging.error(f"Error in cmd_analytics: {e}")
        await message.answer("❌ Произошла ошибка при получении аналитики. Пожалуйста, попробуйте позже.")

@router.message(Command("detailed_analytics"))
async def cmd_detailed_analytics(message: Message):
    """Show detailed analytics"""
    logging.info(f"Received /detailed_analytics command from user {message.from_user.id}")
    try:
        user_id = message.from_user.id
        
        # Get user profile
        profile = db.get_profile(user_id)
        if not profile:
            await message.answer(
                "❌ У вас еще нет профиля. Пожалуйста, создайте его с помощью команды /profile"
            )
            return
        
        # Get subscription status
        is_subscribed = db.get_subscription_status(user_id)
        
        # Get generation history
        history = db.get_generation_history(user_id)
        
        # Count generations by day of week
        day_stats = {
            'Понедельник': 0,
            'Вторник': 0,
            'Среда': 0,
            'Четверг': 0,
            'Пятница': 0,
            'Суббота': 0,
            'Воскресенье': 0
        }
        
        # Count generations by time of day
        time_stats = {
            'Утро (6-12)': 0,
            'День (12-18)': 0,
            'Вечер (18-24)': 0,
            'Ночь (0-6)': 0
        }
        
        for h in history:
            dt = datetime.fromtimestamp(h['timestamp'])
            day_stats[dt.strftime('%A')] += 1
            
            hour = dt.hour
            if 6 <= hour < 12:
                time_stats['Утро (6-12)'] += 1
            elif 12 <= hour < 18:
                time_stats['День (12-18)'] += 1
            elif 18 <= hour < 24:
                time_stats['Вечер (18-24)'] += 1
            else:
                time_stats['Ночь (0-6)'] += 1
        
        # Create detailed analytics message
        analytics = (
            "📊 *ДЕТАЛЬНАЯ АНАЛИТИКА:*\n\n"
            f"👤 *Профиль:*\n"
            f"• Возраст: *{profile['age']} лет*\n"
            f"• Вес: *{profile['weight']} кг*\n"
            f"• Рост: *{profile['height']} см*\n"
            f"• Цель: *{GOAL_MAP.get(profile['goal'], profile['goal'])}*\n\n"
            f"🌟 *Статус подписки:* {'Активна' if is_subscribed else 'Неактивна'}\n\n"
            f"📈 *Генерации по дням недели:*\n"
        )
        
        for day, count in day_stats.items():
            analytics += f"• {day}: *{count}*\n"
        
        analytics += f"\n⏰ *Генерации по времени суток:*\n"
        for time, count in time_stats.items():
            analytics += f"• {time}: *{count}*\n"
        
        if len(history) > 1:
            dates = [datetime.fromtimestamp(h['timestamp']) for h in history]
            dates.sort()
            avg_days = (dates[-1] - dates[0]).days / (len(dates) - 1)
            analytics += f"\n📅 *Средняя частота генераций:* {avg_days:.1f} дней"
        
        await message.answer(analytics, parse_mode="Markdown")
        logging.info(f"Successfully sent detailed analytics to user {user_id}")
    except Exception as e:
        logging.error(f"Error in cmd_detailed_analytics: {e}")
        await message.answer("❌ Произошла ошибка при получении детальной аналитики. Пожалуйста, попробуйте позже.")
