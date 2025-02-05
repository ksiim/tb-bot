from aiogram.fsm.state import State, StatesGroup


class ReportState(StatesGroup):
    get_text = State()
    
    
class PotentialHazardState(StatesGroup):
    get_text = State()