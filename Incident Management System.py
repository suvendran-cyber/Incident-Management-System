import uuid
from datetime import datetime

users = []
incidents = []

VALID_ROLES = ["Admin", "Agent", "User"]
VALID_STATUS = ["Open", "In Progress", "Resolved", "Closed"]
VALID_SEVERITY = ["Low", "Medium", "High", "Critical"]

# ---------------- USER MANAGEMENT ----------------
def create_user():
    username = input("Enter username: ").strip()
    role = input("Enter role (Admin/Agent/User): ").strip().title()

    if role not in VALID_ROLES:
        print("Invalid role")
        return

    user_id = len(users) + 1
    users.append({
        "id": user_id,
        "username": username,
        "role": role
    })

    print(f" User created with ID: {user_id}")

def list_users():
    if not users:
        print("No users found")
        return

    print("\n--- Users ---")
    for u in users:
        print(f"ID: {u['id']} | Name: {u['username']} | Role: {u['role']}")

# ---------------- INCIDENT MANAGEMENT ----------------
def create_incident():
    title = input("Title: ").strip()
    desc = input("Description: ").strip()
    severity = input("Severity (Low/Medium/High/Critical): ").strip().title()

    if severity not in VALID_SEVERITY:
        print("Invalid severity")
        return

    incident = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": desc,
        "severity": severity,
        "status": "Open",
        "assigned_to": None,
        "created_at": datetime.now()
    }

    incidents.append(incident)

    print(f"Incident created with ID: {incident['id']}")

def list_incidents():
    if not incidents:
        print("No incidents found")
        return

    print("\n--- Incidents ---")
    for inc in incidents:
        print(f"""
ID: {inc['id']}
Title: {inc['title']}
Severity: {inc['severity']}
Status: {inc['status']}
Assigned To: {inc['assigned_to']}
Created At: {inc['created_at']}
-------------------------""")

def assign_incident():
    inc_id = input("Enter Incident ID: ").strip()

    try:
        user_id = int(input("Enter User ID: "))
    except ValueError:
        print("Invalid User ID")
        return

    # Check user exists
    if not any(u["id"] == user_id for u in users):
        print("User not found")
        return

    for inc in incidents:
        if inc["id"] == inc_id:
            inc["assigned_to"] = user_id
            inc["status"] = "In Progress"
            print("Incident assigned")
            return

    print("Incident not found")

def update_status():
    inc_id = input("Incident ID: ").strip()
    status = input("New Status (Open/In Progress/Resolved/Closed): ").strip().title()

    if status not in VALID_STATUS:
        print("❌ Invalid status")
        return

    for inc in incidents:
        if inc["id"] == inc_id:
            inc["status"] = status
            print("✅ Status updated")
            return

    print("❌ Incident not found")

# ---------------- SLA ----------------
def check_sla():
    inc_id = input("Incident ID: ").strip()

    for inc in incidents:
        if inc["id"] == inc_id:
            now = datetime.now()
            hours = (now - inc["created_at"]).total_seconds() / 3600

            sla_limits = {
                "Critical": 1,
                "High": 4,
                "Medium": 24,
                "Low": 72
            }

            if hours > sla_limits.get(inc["severity"], 24):
                print("SLA BREACHED")
            else:
                print("Within SLA")
            return

    print("Incident not found")

# ---------------- REPORT ----------------
def report():
    total = len(incidents)
    resolved = sum(1 for i in incidents if i["status"] == "Resolved")

    print("\n--- Report ---")
    print(f"Total Incidents: {total}")
    print(f"Resolved Incidents: {resolved}")

# ---------------- MENU ----------------
def menu():
    print("\n===== INCIDENT MANAGEMENT SYSTEM =====")
    print("1. Create User")
    print("2. List Users")
    print("3. Create Incident")
    print("4. List Incidents")
    print("5. Assign Incident")
    print("6. Update Status")
    print("7. Check SLA")
    print("8. Report")
    print("0. Exit")

# ---------------- MAIN ----------------
def main():
    while True:
        menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            create_incident()
        elif choice == "4":
            list_incidents()
        elif choice == "5":
            assign_incident()
        elif choice == "6":
            update_status()
        elif choice == "7":
            check_sla()
        elif choice == "8":
            report()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
