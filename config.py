"""Shared settings for CampusFlow."""

DATA_FILE = "tickets.json"
CATEGORIES = ["Network", "Hardware", "Software", "Other"]
URGENCIES = ["low", "medium", "high"]
PRIORITIES = ["critical", "high", "medium", "low"]
STATUSES = ["open", "in_progress", "resolved"]
FIELDS = ["id", "title", "category", "urgency", "affected_users",
          "priority", "status", "assigned_to"]
NEXT_STATUS = {"open": "in_progress", "in_progress": "resolved",
               "resolved": "open"}
