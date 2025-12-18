"""
Main Module for the Red Light Green Light Game Project.
Contains the entry point for the application.
"""
from RedLightGreenLight.GameApp import GameApp


class Main:
    """
    Main class for application entry.
    Creates an instance of GameApp and starts it.
    """
    def __init__(self):
        pass

    def main(self):
        """
        Entry point of the application.
        Initializes and starts the GameApp.
        """
        game = GameApp()
        game.run()


if __name__ == "__main__":
    main = Main()
    main.main()

