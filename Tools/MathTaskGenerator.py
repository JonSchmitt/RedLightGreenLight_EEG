import random

class MathTaskGenerator:
    """
    Class responsible for generating mental arithmetic tasks.
    Can be used for calibration and in-game mechanics.
    """
    def __init__(self):
        pass

    def generate_task(self):
        """
        Generates a new random math task string.
        """
        ops = ['+', '-', '*']
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(ops)
        
        # Keep multiplication simpler
        if op == '*':
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            
        return f"{a} {op} {b} = ?"
