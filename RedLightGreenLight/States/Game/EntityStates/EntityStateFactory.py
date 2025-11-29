

class EntityStateFactory:
    _idle_state = None
    _walking_state = None
    _attacking_state = None
    _dead_state = None

    @staticmethod
    def create_idle_state():
        if not EntityStateFactory._idle_state:
            from RedLightGreenLight.States.Game.EntityStates.IdleEntityState import IdleEntityState
            EntityStateFactory._idle_state = IdleEntityState()
        return EntityStateFactory._idle_state

    @staticmethod
    def create_walking_state():
        if not EntityStateFactory._walking_state:
            from RedLightGreenLight.States.Game.EntityStates.WalkingEntityState import WalkingEntityState
            EntityStateFactory._walking_state = WalkingEntityState()
        return EntityStateFactory._walking_state

    @staticmethod
    def create_dead_state():
        if not EntityStateFactory._dead_state:
            from RedLightGreenLight.States.Game.EntityStates.DeadEntityState import DeadEntityState
            EntityStateFactory._dead_state = DeadEntityState()
        return EntityStateFactory._dead_state