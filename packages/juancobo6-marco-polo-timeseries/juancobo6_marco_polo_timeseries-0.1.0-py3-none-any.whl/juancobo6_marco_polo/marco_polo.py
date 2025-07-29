"""Marco Polo game."""

import pandas as pd


def marco_polo(name: str, time: pd.Timestamp) -> str | None:
    """Returns "Polo" if the name is "Marco", otherwise returns None.

    Example:
        >>> marco_polo("Marco", pd.Timestamp("2025-01-01 11:00:00"))
        "Polo"
        >>> marco_polo("John", pd.Timestamp("2025-01-01 11:00:00"))
        None

    Args:
        name (str): The name to check.
        time (pd.Timestamp): The time to check.

    Returns:
        str | None: "Polo" if the name is "Marco", otherwise None.
    """
    _ = pd.DataFrame()

    if time.hour < 12 and name == "Marco":
        return "Polo"

    return None
