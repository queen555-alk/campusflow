"""CampusFlow text-based IT help desk. Run: python helpdesk.py"""

from config import CATEGORIES, DATA_FILE, FIELDS, URGENCIES
from storage import load_tickets, save_tickets
from ticket_service import (
    assign_ticket, change_status, create_ticket, find_ticket, report, work_queue,
)
from validation import clean_choice, clean_title, clean_users

MENU = """
===== CampusFlow Help Desk =====
1. Create ticket
2. List all tickets
3. View one ticket
4. Assign ticket
5. Start work  (open -> in_progress)
6. Resolve     (in_progress -> resolved)
7. Reopen      (resolved -> open)
8. Work queue
9. Reports
0. Exit"""


def ask(prompt, cleaner):
    while True:
        try:
            return cleaner(input(prompt))
        except ValueError as error:
            print(f"  Error: {error}")


def print_tickets(tickets):
    if not tickets:
        print("No tickets to show.")
        return
    print(f"{'ID':<6}{'Title':<28}{'Category':<10}{'Urgency':<8}{'Users':>5}  "
          f"{'Priority':<9}{'Status':<12}Assigned to")
    for t in tickets:
        print(f"{t['id']:<6}{t['title'][:26]:<28}{t['category']:<10}{t['urgency']:<8}"
              f"{t['affected_users']:>5}  {t['priority']:<9}{t['status']:<12}"
              f"{t['assigned_to'] or '-'}")


def main():
    try:
        tickets = load_tickets()
    except ValueError as error:
        print(f"Error: {error}")
        return

    save_after = {"1", "4", "5", "6", "7"}
    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye.")
                break
            if choice == "1":
                title = ask("Title: ", clean_title)
                category = ask(f"Category ({'/'.join(CATEGORIES)}): ",
                               lambda v: clean_choice(v, CATEGORIES, "category"))
                urgency = ask(f"Urgency ({'/'.join(URGENCIES)}): ",
                              lambda v: clean_choice(v, URGENCIES, "urgency"))
                users = ask("Affected users: ", clean_users)
                ticket = create_ticket(tickets, title, category, urgency, users)
                print(f"Created {ticket['id']} with priority '{ticket['priority']}'.")
            elif choice == "2":
                print_tickets(tickets)
            elif choice == "3":
                ticket = find_ticket(tickets, input("Ticket ID: "))
                for field in FIELDS:
                    value = ticket[field]
                    print(f"  {field:<15}: {value if value is not None else '(unassigned)'}")
            elif choice == "4":
                ticket_id = input("Ticket ID: ")
                find_ticket(tickets, ticket_id)
                ticket = assign_ticket(tickets, ticket_id, input("Assign to: "))
                print(f"{ticket['id']} assigned to {ticket['assigned_to']}.")
            elif choice in ("5", "6", "7"):
                status = {"5": "in_progress", "6": "resolved", "7": "open"}[choice]
                ticket = change_status(tickets, input("Ticket ID: "), status)
                print(f"{ticket['id']} is now {ticket['status']}.")
            elif choice == "8":
                print_tickets(work_queue(tickets))
            elif choice == "9":
                summary = report(tickets)
                print(f"\nTotal tickets: {summary['total']}")
                print("By status:  ", ", ".join(f"{k}: {v}" for k, v in summary["status"].items()))
                print("By priority:", ", ".join(f"{k}: {v}" for k, v in summary["priority"].items()))
            else:
                print("Invalid choice. Enter a number from the menu.")
                continue

            if choice in save_after:
                save_tickets(tickets)
        except ValueError as error:
            print(f"Error: {error}")
        except OSError as error:
            print(f"Error: could not save to {DATA_FILE}: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()
