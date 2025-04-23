from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from bot.keyboards.inline import get_goal_keyboard, get_dietary_restrictions_keyboard
from bot.services.database import DatabaseService
import logging

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

class ProfileStates(StatesGroup):
    waiting_for_age = State()
    waiting_for_weight = State()
    waiting_for_height = State()
    waiting_for_goal = State()
    waiting_for_dietary_restrictions = State()

@router.message(Command("profile"))
async def cmd_profile(message: Message, state: FSMContext):
    """Start profile setup"""
    # Check if user already has a profile
    existing_profile = db.get_profile(message.from_user.id)
    if existing_profile:
        # Load existing profile data into state
        await state.update_data(
            age=existing_profile['age'],
            weight=existing_profile['weight'],
            height=existing_profile['height']
        )
        await message.answer(
            "У вас уже есть профиль. Хотите обновить его?",
            reply_markup=get_goal_keyboard()
        )
        await state.set_state(ProfileStates.waiting_for_goal)
        return

    await state.set_state(ProfileStates.waiting_for_age)
    await message.answer(
        "Давайте создадим ваш профиль!\n"
        "Введите ваш возраст (15-100):"
    )

@router.message(ProfileStates.waiting_for_age)
async def process_age(message: Message, state: FSMContext):
    """Process age input"""
    try:
        age = int(message.text)
        if not (15 <= age <= 100):
            raise ValueError
        await state.update_data(age=age)
        await state.set_state(ProfileStates.waiting_for_weight)
        await message.answer(
            "Отлично! Теперь введите ваш вес в килограммах (30-180):"
        )
    except ValueError:
        await message.answer(
            "Пожалуйста, введите корректный возраст (15-100):"
        )

@router.message(ProfileStates.waiting_for_weight)
async def process_weight(message: Message, state: FSMContext):
    """Process weight input"""
    try:
        weight = int(message.text)
        if not (30 <= weight <= 180):
            raise ValueError
        await state.update_data(weight=weight)
        await state.set_state(ProfileStates.waiting_for_height)
        await message.answer(
            "Отлично! Теперь введите ваш рост в сантиметрах (140-200):"
        )
    except ValueError:
        await message.answer(
            "Пожалуйста, введите корректный вес (30-180 кг):"
        )

@router.message(ProfileStates.waiting_for_height)
async def process_height(message: Message, state: FSMContext):
    """Process height input"""
    try:
        height = int(message.text)
        if not (140 <= height <= 200):
            raise ValueError
        await state.update_data(height=height)
        await state.set_state(ProfileStates.waiting_for_goal)
        await message.answer(
            "Отлично! Теперь выберите вашу цель:",
            reply_markup=get_goal_keyboard()
        )
    except ValueError:
        await message.answer(
            "Пожалуйста, введите корректный рост (140-200 см):"
        )

@router.callback_query(ProfileStates.waiting_for_goal)
async def process_goal(callback: CallbackQuery, state: FSMContext):
    """Process goal selection"""
    try:
        goal = callback.data.split(":")[1]
        logging.info(f"Selected goal: {goal}")
        await state.update_data(goal=goal)
        await state.set_state(ProfileStates.waiting_for_dietary_restrictions)
        await callback.message.answer(
            "Выберите пищевые ограничения:",
            reply_markup=get_dietary_restrictions_keyboard()
        )
    except Exception as e:
        logging.error(f"Error in process_goal: {e}")
        await callback.message.answer(
            "❌ Произошла ошибка при обработке выбора. Пожалуйста, попробуйте снова.",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.clear()

@router.callback_query(ProfileStates.waiting_for_dietary_restrictions)
async def process_dietary_restrictions(callback: CallbackQuery, state: FSMContext):
    """Process dietary restrictions selection"""
    try:
        # Get the dietary restriction from callback data
        dietary_restrictions = callback.data.split(":")[1]
        logging.info(f"Selected dietary restrictions: {dietary_restrictions}")
        
        # Get all profile data
        profile_data = await state.get_data()
        logging.info(f"Current profile data: {profile_data}")
        
        # Save profile to database
        if db.save_profile(callback.from_user.id, profile_data):
            logging.info("Profile saved successfully")
            # Create profile summary message with readable values
            profile_summary = (
                "✅ Ваш профиль успешно сохранен!\n\n"
                f"📊 Ваш профиль:\n"
                f"👤 Возраст: {profile_data['age']} лет\n"
                f"⚖️ Вес: {profile_data['weight']} кг\n"
                f"📏 Рост: {profile_data['height']} см\n"
                f"🎯 Цель: {GOAL_MAP.get(profile_data['goal'], profile_data['goal'])}\n"
                f"🥗 Пищевые ограничения: {DIET_MAP.get(dietary_restrictions, dietary_restrictions)}\n\n"
                "Вы можете изменить профиль в любой момент, используя команду /profile"
            )
            
            await callback.message.answer(
                profile_summary,
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            logging.error("Failed to save profile")
            await callback.message.answer(
                "❌ Произошла ошибка при сохранении профиля. Пожалуйста, попробуйте позже.",
                reply_markup=ReplyKeyboardRemove()
            )
    except Exception as e:
        logging.error(f"Error in process_dietary_restrictions: {e}")
        await callback.message.answer(
            "❌ Произошла ошибка при обработке выбора. Пожалуйста, попробуйте снова.",
            reply_markup=ReplyKeyboardRemove()
        )
    
    await state.clear() 