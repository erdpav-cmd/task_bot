from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import FSInputFile
from database import Database

# Создаем роутер
router = Router()

# Инициализируем объект БД
db = Database()

# Машина состояний (FSM)
class TaskStates(StatesGroup):
    waiting_for_text = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Команда /start: приветствие и подсказка"""
    await message.answer(
        "👋 Привет! Я бот для хранения задач команды.\n"
        "Используй:\n"
        "➕ /add — добавить задачу\n"
        "📋 /list — посмотреть все задачи\n"
        "📄 /list_csv — выгрузить задачи в Excel"
    )

@router.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    """Команда /add: переводим бота в режим ожидания текста"""
    await message.answer("✍️ Введите текст задачи:")
    await state.set_state(TaskStates.waiting_for_text)

@router.message(TaskStates.waiting_for_text)
async def process_add_task(message: types.Message, state: FSMContext):
    """Получаем текст задачи, сохраняем в БД и сбрасываем состояние"""
    task_text = message.text
    username = message.from_user.username or message.from_user.first_name
    
    task_id = db.add_task(task_text, username)
    await message.answer(f"✅ Задача #{task_id} сохранена!")
    await state.clear()

@router.message(Command("list"))
async def cmd_list(message: types.Message):
    """Команда /list: выводим список задач"""
    tasks = db.get_all_tasks()
    if not tasks:
        await message.answer("📭 Список задач пуст.")
        return

    response = "📋 Ваши задачи:\n\n"
    for task_id, text, user, created_at in tasks:
        response += f"🔹 #{task_id} | 👤 {user} | 🕒 {created_at}\n📝 {text}\n\n"
    
    await message.answer(response[:4000])

@router.message(Command("list_csv"))
async def cmd_list_csv(message: types.Message):
    """Команда /list_csv: генерируем CSV и отправляем файл"""
    csv_path = db.export_to_csv()
    await message.answer_document(
        FSInputFile(csv_path),
        caption="📄 Вот ваш список задач в CSV."
    )