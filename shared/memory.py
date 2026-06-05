import json
import os

MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "memory.json"
)


def load_memory():

    try:

        with open(
            MEMORY_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return {}


def save_memory(data):

    with open(
        MEMORY_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def remember(key, value):

    memory = load_memory()

    memory[key] = value

    save_memory(memory)


def recall(key):

    memory = load_memory()

    return memory.get(
        key,
        None
    )