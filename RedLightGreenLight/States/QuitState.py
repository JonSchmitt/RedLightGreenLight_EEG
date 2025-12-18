
from RedLightGreenLight.Inputs.KeysEnum import KEY
from RedLightGreenLight.States.State import State
from RedLightGreenLight.States.StateFactory import StateFactory


class QuitState(State):
    """
    State representing the end of the application.
    """
    def __init__(self):
        super().__init__()


    def update(self,delta_time,keys:list[KEY])->State|None:
        return StateFactory.create_quit_state()