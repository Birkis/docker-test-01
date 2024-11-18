#!/usr/bin/env python
import sys
from .crew import BirthdayPartyPlanningCrew

def run(inputs=None):
    """
    Run the crew.
    """
    if inputs is None:
        inputs = {"company": "Bunnies AI", "age": "10", "interests": "dinosaurs and science"}
    result = BirthdayPartyPlanningCrew().crew().kickoff(inputs=inputs)
    return result

if __name__ == "__main__":
    run()
