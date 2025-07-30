from typing import Tuple

def convert_to_human_size(number: float) -> Tuple[float, str]:
    UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    unit = UNITS[0]
    for unit in UNITS:
        if float(number) < 1024.0:
            return number, unit
        number = round(float(number) / 1024.0, 2)
    # Fallback return in case all units are exhausted
    return number, unit

def convert_to_human_number(number: float) -> Tuple[float, str]:
    UNITS = ["", "K", "M", "G", "T", "P"]
    unit = UNITS[0]
    for unit in UNITS:
        if float(number) < 1000.0:
            return number, unit
        number = round(float(number) / 1000.0, 2)
    # Fallback return in case all units are exhausted
    return number, unit
