from agents import function_tool
import random

@function_tool
def roll_dice()->str:
    return f"you roll a dice{random.randint(1,6)}!"

@function_tool
def generate_events()->str :
    events =[
        "you encountered a dragon",
        "you found a treasure chest",
        "you fell into a trap",
        "you met a mysterious wizard"
    ]

    return random.choice(events)