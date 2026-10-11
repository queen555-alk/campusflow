"""Ticket creation, assignment, workflow, queue and reports."""

from config import CATEGORIES, NEXT_STATUS, PRIORITIES, STATUSES, URGENCIES
from validation import clean_choice, clean_title, clean_users


def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def create_ticket(tickets, title, category, urgency, users):
    title = clean_title(title)
    category = clean_choice(category, CATEGORIES, "category")
    urgency = clean_choice(urgency, URGENCIES, "urgency")
    users = clean_users(users)
    number = max((int(t["id"][1:]) for t in tickets), default=0) + 1

    ticket = {
        "id": f"T{number:03d}", "title": title, "category": category,
        "urgency": urgency, "affected_users": users,
        "priority": calculate_priority(urgency, users),
        "status": "open", "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def find_ticket(tickets, ticket_id):
    ticket_id = str(ticket_id).strip().upper()
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ValueError(f"Unknown ticket ID '{ticket_id}'.")


def assign_ticket(tickets, ticket_id, name):
    ticket = find_ticket(tickets, ticket_id)
    name = str(name).strip()
    if not name:
        raise ValueError("Staff member name must not be blank.")
    if ticket["status"] == "resolved":
        raise ValueError(f"{ticket['id']} is resolved. Reopen it before changing it.")
    ticket["assigned_to"] = name
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    allowed = NEXT_STATUS[ticket["status"]]
    if allowed != new_status:
        raise ValueError(
            f"{ticket['id']} is '{ticket['status']}'; it can only move to '{allowed}'."
        )
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError(f"{ticket['id']} is unassigned. Assign it before starting work.")
    ticket["status"] = new_status
    return ticket


def work_queue(tickets):
    pending = [t for t in tickets if t["status"] != "resolved"]
    return sorted(pending, key=lambda t: (PRIORITIES.index(t["priority"]), int(t["id"][1:])))


def report(tickets):
    return {
        "total": len(tickets),
        "status": {s: sum(t["status"] == s for t in tickets) for s in STATUSES},
        "priority": {p: sum(t["priority"] == p for t in tickets) for p in PRIORITIES},
    }
