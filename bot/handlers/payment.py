from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.services.database import DatabaseService
from bot.keyboards.inline import get_subscription_keyboard

router = Router()
db = DatabaseService()

@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    """Show subscription options"""
    await message.answer(
        "🌟 Подписка на премиум-функции:\n\n"
        "✅ Неограниченная генерация планов\n"
        "✅ Доступ к недельным планам\n"
        "✅ Приоритетная поддержка\n\n"
        "Выберите тариф:",
        reply_markup=get_subscription_keyboard()
    )

@router.callback_query(F.data.startswith("subscribe:"))
async def process_subscription(callback: CallbackQuery):
    """Process subscription selection"""
    plan = callback.data.split(":")[1]
    
    # Здесь будет логика оплаты через Telegram Payments
    # Пока просто обновляем статус подписки в базе
    if db.update_subscription(callback.from_user.id, plan):
        await callback.message.answer(
            "✅ Спасибо за подписку! Теперь вам доступны все премиум-функции."
        )
    else:
        await callback.message.answer(
            "❌ Произошла ошибка при оформлении подписки. Пожалуйста, попробуйте позже."
        ) 