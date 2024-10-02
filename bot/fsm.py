from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis

redis = Redis(host='localhost', port=6379, db=1)

storage = RedisStorage(redis=redis)


class FSMSolveTask(StatesGroup):
    get_answer = State()
