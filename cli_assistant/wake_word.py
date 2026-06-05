"""Wake-word detection with speech-to-text tolerance."""

WAKE_PHRASE = "harry potter"

# Common mis-hearings from Google Speech (en-IN / en-US)
WAKE_ALIASES = (
    "harry potter",
    "hari potter",
    "harry hotter",
    "harry pota",
    "hey harry potter",
    "hey harry",
    "harry",
)


def is_wake_command(command: str) -> bool:
    if not command:
        return False
    cmd = command.lower().strip()
    for alias in WAKE_ALIASES:
        if alias in cmd:
            return True
    # "harry" + "potter" anywhere in the phrase
    if "harry" in cmd and "potter" in cmd:
        return True
    if "hari" in cmd and "potter" in cmd:
        return True
    return False
