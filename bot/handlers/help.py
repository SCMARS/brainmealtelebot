from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command"""
    help_text = (
        "👋 *Привет! Я твой персональный помощник по питанию.*\n\n"
        "📋 *Доступные команды:*\n\n"
        "👤 */profile* - Создать или обновить профиль\n"
        "   • Возраст (15-100 лет)\n"
        "   • Вес (30-180 кг)\n"
        "   • Рост (140-200 см)\n"
        "   • Цель (похудение/набор массы/поддержание)\n\n"
        "🍽️ */generateforday* - Сгенерировать план питания на день\n"
        "   • Выберите тип питания\n"
        "   • Укажите желаемое количество калорий (1000-5000)\n\n"
        "📅 */generateforweek* - Сгенерировать план питания на неделю\n"
        "   • Требуется подписка\n"
        "   • Выберите тип питания\n"
        "   • Укажите желаемое количество калорий (1000-5000)\n\n"
        "🌟 */subscribe* - Оформить подписку\n"
        "   • Месяц - 299₽\n"
        "   • 3 месяца - 799₽\n"
        "   • Год - 2999₽\n\n"
        "📊 */analytics* - Просмотр базовой аналитики\n"
        "   • Статистика генераций\n"
        "   • Распределение по типам планов\n\n"
        "📈 */detailed_analytics* - Просмотр детальной аналитики\n"
        "   • Генерации по дням недели\n"
        "   • Генерации по времени суток\n"
        "   • Средняя частота генераций\n\n"
        "❓ */help* - Показать это сообщение\n\n"
        "💡 *Подсказка:* Начните с создания профиля (/profile), затем используйте /generateforday для генерации плана питания."
    )
    
    await message.answer(help_text, parse_mode="Markdown")