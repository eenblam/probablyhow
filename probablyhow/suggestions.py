from random import choice

SUGGESTED_TASKS = [
        "hack the planet",
        "taste my teeth",
        "turn off a banana"
        ]

def random_task():
    return choice(SUGGESTED_TASKS)
