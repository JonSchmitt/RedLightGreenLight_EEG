import pygame

from RedLightGreenLight.Inputs.KeysEnum import KEY


class InputManager:
    def __init__(self):
        pass

    def process_inputs(self)->list[list[KEY]]:
        inputs = []
        inputs.append(self._process_pressed_keys())
        inputs.append(self._process_keydown())
        return inputs

    def _process_pressed_keys(self)->list[KEY]:
        keys_pressed = []
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            keys_pressed.append(KEY.ESC)
        if keys[pygame.K_SPACE]:
            keys_pressed.append(KEY.SPACE)
        if keys[pygame.K_RIGHT]:
            keys_pressed.append(KEY.RIGHT)

        return keys_pressed

    def _process_keydown(self)->list[KEY]:
        keys_down = []
        keys = pygame.event.get([pygame.KEYDOWN])
        for key in keys:
            if key.key == pygame.K_ESCAPE:
                keys_down.append(KEY.ESC)
            if key.key == pygame.K_SPACE:
                keys_down.append(KEY.SPACE)
            if key.key == pygame.K_RIGHT:
                keys_down.append(KEY.RIGHT)
        return keys_down