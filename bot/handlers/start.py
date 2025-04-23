from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command"""
    await message.answer(
        "👋 Привет! Я твой персональный помощник по питанию.\n\n"
        "Я помогу тебе составить план питания на основе твоих целей и предпочтений.\n\n"
        "Доступные команды:\n"
        "/profile - Настроить профиль\n"
        "/generateforday - Сгенерировать план на день\n"
        "/generateforweek - Сгенерировать план на неделю\n"
        "/subscribe - Подписаться на премиум\n"
        "/help - Помощь\n"
        "/analize - Анализатор питания\n"
    ) 