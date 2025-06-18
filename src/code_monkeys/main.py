#!/usr/bin/env python
import warnings
from datetime import datetime
from code_monkeys.crew import CodeMonkeys

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """Run the CodeMonkeys crew"""
    inputs = {'assignment': """Write a python version of the hangman game. There should be at least 50 words. 
              When game starts, randomly select one of the words. Use ascii art to 'draw' the hanging man, 
              and update the drawing each wrong guess"""}
    result = CodeMonkeys().crew().kickoff(inputs=inputs)
    print(result.raw)
