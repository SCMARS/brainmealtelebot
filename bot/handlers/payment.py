from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from bot.services.database import DatabaseService
from bot.keyboards.inline import get_subscription_keyboard
from bot.config import (
    PAYMENT_TOKEN,
    SUBSCRIPTION_PRICES,
    SUBSCRIPTION_TITLES,
    SUBSCRIPTION_DESCRIPTIONS,
    SUBSCRIPTION_DURATIONS
)
import logging

router = Router()
db = DatabaseService()

@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    """Show subscription options"""
    # Определяем язык пользователя по его локали
    user_language = message.from_user.language_code
    is_ukrainian = user_language == 'uk'
    
    currency = 'UAH' if is_ukrainian else 'RUB'
    
    # Формируем сообщение на нужном языке
    if is_ukrainian:
        text = (
            "🌟 Підписка на преміум-функції:\n\n"
            "✅ Необмежена генерація планів\n"
            "✅ Доступ до тижневих планів\n"
            "✅ Пріоритетна підтримка\n\n"
            "Виберіть тариф:"
        )
    else:
        text = (
            "🌟 Подписка на премиум-функции:\n\n"
            "✅ Неограниченная генерация планов\n"
            "✅ Доступ к недельным планам\n"
            "✅ Приоритетная поддержка\n\n"
            "Выберите тариф:"
        )
    
    await message.answer(
        text,
        reply_markup=get_subscription_keyboard(currency)
    )

@router.callback_query(F.data.startswith("subscribe:"))
async def process_subscription(callback: CallbackQuery):
    """Process subscription selection"""
    # Определяем язык пользователя
    user_language = callback.from_user.language_code
    is_ukrainian = user_language == 'uk'
    currency = 'UAH' if is_ukrainian else 'RUB'
    
    plan = callback.data.split(":")[1]
    
    if plan not in SUBSCRIPTION_PRICES[currency]:
        await callback.message.answer(
            "❌ Неверный тариф подписки" if not is_ukrainian else "❌ Невірний тариф підписки"
        )
        return
    
    # Создаем инвойс для оплаты
    await callback.message.answer_invoice(
        title=SUBSCRIPTION_TITLES[currency][plan],
        description=SUBSCRIPTION_DESCRIPTIONS[currency][plan],
        provider_token=PAYMENT_TOKEN,
        currency=currency,
        prices=[
            LabeledPrice(
                label=SUBSCRIPTION_TITLES[currency][plan],
                amount=SUBSCRIPTION_PRICES[currency][plan]
            )
        ],
        payload=f"subscription:{plan}:{currency}"
    )

@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    """Process pre-checkout query"""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    """Process successful payment"""
    try:
        # Получаем тип подписки и валюту из payload
        _, plan, currency = message.successful_payment.invoice_payload.split(":")
        
        # Обновляем статус подписки в базе
        if db.update_subscription(
            message.from_user.id,
            plan,
            SUBSCRIPTION_DURATIONS[plan]
        ):
            # Определяем язык пользователя
            user_language = message.from_user.language_code
            is_ukrainian = user_language == 'uk'
            
            if is_ukrainian:
                success_message = (
                    "✅ Дякуємо за підписку! Тепер вам доступні всі преміум-функції.\n\n"
                    "Ви можете використовувати:\n"
                    "• Необмежену генерацію планів\n"
                    "• Доступ до тижневих планів\n"
                    "• Пріоритетну підтримку"
                )
            else:
                success_message = (
                    "✅ Спасибо за подписку! Теперь вам доступны все премиум-функции.\n\n"
                    "Вы можете использовать:\n"
                    "• Неограниченную генерацию планов\n"
                    "• Доступ к недельным планам\n"
                    "• Приоритетную поддержку"
                )
            
            await message.answer(success_message)
        else:
            error_message = (
                "❌ Произошла ошибка при активации подписки. Пожалуйста, обратитесь в поддержку."
                if not is_ukrainian else
                "❌ Сталася помилка при активації підписки. Будь ласка, зверніться до підтримки."
            )
            await message.answer(error_message)
    except Exception as e:
        logging.error(f"Error processing payment: {e}")
        error_message = (
            "❌ Произошла ошибка при обработке платежа. Пожалуйста, обратитесь в поддержку."
            if not is_ukrainian else
            "❌ Сталася помилка при обробці платежу. Будь ласка, зверніться до підтримки."
        )
        await message.answer(error_message) 