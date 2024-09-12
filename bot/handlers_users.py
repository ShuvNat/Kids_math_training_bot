from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from fsm import FSMSolveTask
from keyboards import keyboard
from lexicon import LEXICON
from tasks import Tasks

user_router = Router()


# обработчик команды start
@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    await message.answer(text=LEXICON['/start'])


# обработчик команды task в основном режиме выдает клавиатуру в выбором задачи
@user_router.message(Command(commands='task'), StateFilter(default_state))
async def cmd_task(message: Message):
    await message.answer(
        text=LEXICON['/task'],
        reply_markup=keyboard
    )


# обработчик команды cancel в основном режиме
@user_router.message(Command(commands='cancel'), StateFilter(default_state))
async def cmd_cancel(message: Message):
    await message.answer(text=LEXICON['/cancel'])


# обработчик команды calcel в режиме задачи
@user_router.message(Command(commands='cancel'), StateFilter(FSMSolveTask.get_answer))
async def cmd_cancel_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['/cancel_state'],
                         reply_markup=keyboard)
    await state.clear()


# обработчик команды task в режиме решения
@user_router.callback_query(~StateFilter(default_state))
async def get_task_state(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON['/task_state'])
    await callback.answer()


# обработчик выдающий задачу
@user_router.callback_query(StateFilter(default_state))
async def get_task(callback: CallbackQuery, state: FSMContext):
    task = Tasks()
    func = getattr(task, callback.data)
    func()
    await state.update_data(answer=task.answer)
    await callback.message.answer(
            text=f'{task.question}'
        )
    await state.set_state(FSMSolveTask.get_answer)
    await callback.answer()


# обработчик проверяющий ответ и отправляющий результат в бд
@user_router.message(StateFilter(FSMSolveTask.get_answer))
async def check_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_answer = data.get('answer')
    user_answer = message.text

    if user_answer.isdigit() and int(user_answer) == correct_answer:
        await message.answer(text=LEXICON['right'])
        await message.answer(text=LEXICON['one_more'],
                             reply_markup=keyboard)
        await state.clear()
    else:
        await message.answer(text=LEXICON['wrong'])
