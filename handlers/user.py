from aiogram import F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, FSInputFile
)

from bot import dp, bot

from models.dbs.orm import Orm
from models.dbs.models import *

from .callbacks import *
from .markups import *
from .states import *

@dp.message(Command('start'))
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()
    
    await Orm.create_user(message)
    await send_start_message(message)
    
async def send_start_message(message: Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=await generate_start_text(message),
        reply_markup=start_markup
    )
    
@dp.message(F.text == security_rules_label)
async def security_rules_message_handler(message: Message):
    await message.answer(
        text=(await Orm.get_text_by_name('rules')).text
    )
    
@dp.message(F.text == alert_potential_hazard_label)
async def alert_potential_hazard_message_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Опишите потенциальную опасность",
    )
    
    await state.set_state(PotentialHazardState.get_text)


@dp.message(F.text == upload_report_label)
async def upload_report_message_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Загрузите отчет текстом",
    )
    
    await state.set_state(ReportState.get_text)
    
@dp.message(ReportState.get_text)
async def report_message_handler(message: Message, state: FSMContext):
    
    await Orm.add_item(
        Report(
            user_id=message.from_user.id,
            text=message.text
        )
    )
    
    await message.answer(
        text="Отчет успешно загружен",
        reply_markup=start_markup
    )
    
    await send_text_to_admins(
        text=f"Пользователь {message.from_user.full_name} ({message.from_user.id}) загрузил отчет:\n\n {message.text}"
    )
    
    await state.clear()
    
@dp.message(PotentialHazardState.get_text)
async def potential_hazard_message_handler(message: Message, state: FSMContext):
    
    await Orm.add_item(
        PotentialHazard(
            user_id=message.from_user.id,
            text=message.text
        )
    )
    
    await message.answer(
        text="Потенциальная опасность успешно отправлена",
        reply_markup=start_markup
    )
    
    await send_text_to_admins(
        text=f"Пользователь {message.from_user.full_name} ({message.from_user.id}) отправил сообщение о потенциальной опасности:\n\n {message.text}"
    )
    
    await state.clear()
    
async def send_text_to_admins(text):
    admins = await Orm.get_all_admins()
    
    for admin in admins:
        await bot.send_message(
            chat_id=admin.telegram_id,
            text=text
        )
        
@dp.message(Command('getmyadmin'))
async def get_my_admin_message_handler(message: Message):
    await Orm.turn_to_admin(message.from_user.id)
    
    await message.answer(
        text="Теперь вы администратор"
    )
        
    