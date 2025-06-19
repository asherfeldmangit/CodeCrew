#!/usr/bin/env python
import warnings
import os
from code_monkeys.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

os.makedirs('output', exist_ok=True)

requirements = """Create the game tic tac toe. The game should allow 1 user to play against the 'machine', OR two players to play eachother"""
module_name = "TicTacToe"
class_name = "T3Game"


def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    run()
