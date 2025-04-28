from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.services.database import DatabaseService
from bot.services.gemini import GeminiService
from bot.keyboards.inline import get_meal_type_keyboard
import logging

router = Router()
db = DatabaseService()
gemini = GeminiService()

class GenerateStates(StatesGroup):
    waiting_for_meal_type = State()
    waiting_for_calories = State()

@router.message(Command("generateforday"))
async def cmd_generate_day(message: Message, state: FSMContext):
    """Start daily meal plan generation"""
    # Check if user has a profile
    profile = db.get_profile(message.from_user.id)
    if not profile:
        await message.answer(
            "❌ У вас еще нет профиля. Пожалуйста, создайте его с помощью команды /profile"
        )
        return

    # Get existing meals for the day
    existing_meals = db.get_user_meals(message.from_user.id, limit=5)  # Get last 5 meals

    await state.set_state(GenerateStates.waiting_for_meal_type)
    await message.answer(
        "Выберите тип плана питания:",
        reply_markup=get_meal_type_keyboard()
    )

@router.message(Command("generateforweek"))
async def cmd_generate_week(message: Message, state: FSMContext):
    """Start weekly meal plan generation"""
    # Check if user has a profile
    profile = db.get_profile(message.from_user.id)
    if not profile:
        await message.answer(
            "❌ У вас еще нет профиля. Пожалуйста, создайте его с помощью команды /profile"
        )
        return

    # Check subscription
    if not db.get_subscription_status(message.from_user.id):
        await message.answer(
            "❌ Генерация недельного плана доступна только для подписчиков.\n"
            "Используйте команду /subscribe для оформления подписки."
        )
        return

    # Get existing meals for the week
    existing_meals = db.get_user_meals(message.from_user.id, limit=20)  # Get last 20 meals

    await state.set_state(GenerateStates.waiting_for_meal_type)
    await message.answer(
        "Выберите тип плана питания:",
        reply_markup=get_meal_type_keyboard()
    )

@router.callback_query(GenerateStates.waiting_for_meal_type)
async def process_meal_type(callback: CallbackQuery, state: FSMContext):
    """Process meal type selection"""
    meal_type = callback.data.split(":")[1]
    await state.update_data(meal_type=meal_type)
    await state.set_state(GenerateStates.waiting_for_calories)
    
    await callback.message.answer(
        "Введите желаемое количество калорий в день (например, 2000):"
    )

@router.message(GenerateStates.waiting_for_calories)
async def process_calories(message: Message, state: FSMContext):
    """Process calories input and generate meal plan"""
    try:
        calories = int(message.text)
        if not (1000 <= calories <= 5000):
            raise ValueError
            
        # Get user profile
        profile = db.get_profile(message.from_user.id)
        if not profile:
            await message.answer("❌ Профиль не найден. Используйте /profile для создания профиля.")
            await state.clear()
            return
            
        # Get meal type from state
        data = await state.get_data()
        meal_type = data.get('meal_type', 'balanced')
        
        # Check if this is a weekly plan
        is_weekly = message.text.startswith('/generateforweek')
        
        # Check subscription for weekly plan
        if is_weekly and not db.get_subscription_status(message.from_user.id):
            await message.answer(
                "❌ Генерация недельного плана доступна только для подписчиков.\n"
                "Используйте команду /subscribe для оформления подписки."
            )
            await state.clear()
            return
        
        # Generate meal plan
        await message.answer("🔄 Генерирую план питания...")
        
        # Add calories to profile
        profile['calories'] = calories
        
        # Get existing meals
        existing_meals = db.get_user_meals(message.from_user.id, limit=20 if is_weekly else 5)
        
        # Generate meal plan
        meal_plan = await gemini.generate_meal_plan(profile, 7 if is_weekly else 1, existing_meals)
        
        # Check if response is an error message
        if meal_plan.startswith("❌"):
            await message.answer(meal_plan)
            await state.clear()
            return
        
        # Split long message if needed
        if len(meal_plan) > 4000:
            parts = [meal_plan[i:i+4000] for i in range(0, len(meal_plan), 4000)]
            for part in parts:
                await message.answer(part)
        else:
            await message.answer(meal_plan)
            
        # Save generation history
        db.save_generation(
            message.from_user.id,
            'weekly' if is_weekly else 'daily',
            calories
        )
            
        await state.clear()
        
    except ValueError:
        await message.answer(
            "Пожалуйста, введите корректное количество калорий (1000-5000):"
        ) 