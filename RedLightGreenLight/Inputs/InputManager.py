import pygame

from RedLightGreenLight.Inputs.KeysEnum import KEY


class InputManager:
    def __init__(self):
        self._external_keys = []

    def inject_key(self, key: KEY):
        """Allows external processes/threads to inject keys."""
        if key not in self._external_keys:
            self._external_keys.append(key)

    def clear_injected_key(self, key: KEY):
        """Removes an injected key."""
        if key in self._external_keys:
            self._external_keys.remove(key)

    def process_inputs(self)->list[list[KEY]]:
        inputs = []
        
        # Physical keys
        pressed = self._process_pressed_keys()
        keydown = self._process_keydown()
        
        # Merge with external keys
        # for process_pressed_keys style (continuous)
        pressed.extend(self._external_keys)
        # remove duplicates
        pressed = list(set(pressed))
        
        inputs.append(pressed)
        inputs.append(keydown)
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