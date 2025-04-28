from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_goal_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for goal selection"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="Похудение",
                callback_data="goal:lose_weight"
            )
        ],
        [
            InlineKeyboardButton(
                text="Набор массы",
                callback_data="goal:gain_muscle"
            )
        ],
        [
            InlineKeyboardButton(
                text="Поддержание",
                callback_data="goal:maintain"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_meal_type_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for meal type selection"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="Сбалансированное питание",
                callback_data="meal:balanced"
            )
        ],
        [
            InlineKeyboardButton(
                text="Высокобелковое",
                callback_data="meal:high_protein"
            )
        ],
        [
            InlineKeyboardButton(
                text="Низкоуглеводное",
                callback_data="meal:low_carb"
            )
        ],
        [
            InlineKeyboardButton(
                text="Средиземноморское",
                callback_data="meal:mediterranean"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_subscription_keyboard(currency: str = 'RUB') -> InlineKeyboardMarkup:
    """Create keyboard for subscription selection"""
    if currency == 'UAH':
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Місяць - 120₴",
                    callback_data="subscribe:month"
                )
            ],
            [
                InlineKeyboardButton(
                    text="3 місяці - 320₴",
                    callback_data="subscribe:quarter"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Рік - 1200₴",
                    callback_data="subscribe:year"
                )
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    text="Месяц - 299₽",
                    callback_data="subscribe:month"
                )
            ],
            [
                InlineKeyboardButton(
                    text="3 месяца - 799₽",
                    callback_data="subscribe:quarter"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Год - 2999₽",
                    callback_data="subscribe:year"
                )
            ]
        ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 