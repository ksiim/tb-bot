from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot import bot

from .callbacks import *


async def generate_start_text(message):
    return f"Привет, {message.from_user.full_name}! Я - бот"

security_rules_label = "Правила безопасности"
alert_potential_hazard_label = "Сообщить о потенциальной опасности"
upload_report_label = "Загрузить отчет"

start_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=security_rules_label),
        ],
        [
            KeyboardButton(text=alert_potential_hazard_label),
            KeyboardButton(text=upload_report_label),
        ]
    ],
    resize_keyboard=True,
)
