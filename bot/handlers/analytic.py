from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.services.database import DatabaseService
from datetime import datetime, timedelta

router = Router()
db = DatabaseService()

# Словари для преобразования технических значений в читаемые
GOAL_MAP = {
    'lose_weight': 'Похудение',
    'gain_muscle': 'Набор массы',
    'maintain': 'Поддержание'
}

DIET_MAP = {
    'vegan': 'Веган',
    'gluten_free': 'Без глютена',
    'omnivore': 'Всёяден'
}

PLAN_TYPE_MAP = {
    'daily': 'Дневной план',
    'weekly': 'Недельный план'
}

@router.message(Command("analytics"))
async def cmd_analytics(message: Message):
    """Show basic analytics"""
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
        "📊 Ваша аналитика:\n\n"
        f"👤 Профиль:\n"
        f"• Возраст: {profile['age']} лет\n"
        f"• Вес: {profile['weight']} кг\n"
        f"• Рост: {profile['height']} см\n"
        f"• Цель: {GOAL_MAP.get(profile['goal'], profile['goal'])}\n"
        f"• Пищевые ограничения: {DIET_MAP.get(profile['dietary_restrictions'], profile['dietary_restrictions'])}\n\n"
        f"🌟 Статус подписки: {'Активна' if is_subscribed else 'Неактивна'}\n\n"
        f"📈 Статистика генераций:\n"
        f"• Всего сгенерировано: {total_generations}\n"
        f"• За последнюю неделю: {last_week_generations}\n\n"
        f"📊 Распределение по типам планов:\n"
    )
    
    for plan_type, count in plan_types.items():
        analytics += f"• {plan_type}: {count}\n"
    
    analytics += "\nИспользуйте /detailed_analytics для просмотра детальной статистики."
    
    await message.answer(analytics)

@router.message(Command("detailed_analytics"))
async def cmd_detailed_analytics(message: Message):
    """Show detailed analytics"""
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
    
    # Analyze by day of week
    days_of_week = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 
                   3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}
    day_stats = {day: 0 for day in days_of_week.values()}
    
    for h in history:
        day = datetime.fromtimestamp(h['timestamp']).weekday()
        day_stats[days_of_week[day]] += 1
    
    # Analyze by time of day
    time_stats = {'утро': 0, 'день': 0, 'вечер': 0, 'ночь': 0}
    for h in history:
        hour = datetime.fromtimestamp(h['timestamp']).hour
        if 5 <= hour < 12:
            time_stats['утро'] += 1
        elif 12 <= hour < 17:
            time_stats['день'] += 1
        elif 17 <= hour < 23:
            time_stats['вечер'] += 1
        else:
            time_stats['ночь'] += 1
    
    # Create detailed analytics message
    analytics = (
        "📊 Детальная аналитика:\n\n"
        f"👤 Профиль:\n"
        f"• Возраст: {profile['age']} лет\n"
        f"• Вес: {profile['weight']} кг\n"
        f"• Рост: {profile['height']} см\n"
        f"• Цель: {GOAL_MAP.get(profile['goal'], profile['goal'])}\n"
        f"• Пищевые ограничения: {DIET_MAP.get(profile['dietary_restrictions'], profile['dietary_restrictions'])}\n\n"
        f"🌟 Статус подписки: {'Активна' if is_subscribed else 'Неактивна'}\n\n"
        f"📈 Генерации по дням недели:\n"
    )
    
    for day, count in day_stats.items():
        analytics += f"• {day}: {count}\n"
    
    analytics += f"\n⏰ Генерации по времени суток:\n"
    for time, count in time_stats.items():
        analytics += f"• {time}: {count}\n"
    
    if len(history) > 1:
        dates = [datetime.fromtimestamp(h['timestamp']) for h in history]
        dates.sort()
        avg_days = (dates[-1] - dates[0]).days / (len(dates) - 1)
        analytics += f"\n📅 Средняя частота генераций: {avg_days:.1f} дней"
    
    await message.answer(analytics)
