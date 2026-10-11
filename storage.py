"""JSON persistence for tickets."""

import json
import os
from config import DATA_FILE, FIELDS


def save_tickets(tickets, path=DATA_FILE):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=2)


def load_tickets(path=DATA_FILE):
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"'{path}' is not valid JSON ({error}). The file was not changed; "
            "fix or move it, then restart."
        ) from error

    valid = isinstance(tickets, list) and all(
        isinstance(ticket, dict) and set(FIELDS) <= ticket.keys()
        for ticket in tickets
    )
    if not valid:
        raise ValueError(f"'{path}' does not contain valid ticket data. The file was not changed.")
    return tickets
