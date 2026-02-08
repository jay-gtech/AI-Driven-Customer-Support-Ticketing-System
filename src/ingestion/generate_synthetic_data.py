import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

NUM_TICKETS = 1000

CATEGORIES = {
    "Login": [
        "Unable to login with my account",
        "Password reset link not working",
        "Getting invalid credentials error",
        "Account locked after multiple attempts"
    ],
    "Billing": [
        "Charged twice for subscription",
        "Invoice not generated",
        "Payment failed but amount deducted",
        "Need refund for last transaction"
    ],
    "Bug": [
        "App crashes on submit",
        "Page not loading properly",
        "Unexpected error occurred",
        "Feature not working as expected"
    ],
    "Feature Request": [
        "Please add dark mode",
        "Need export to CSV option",
        "Request for API access",
        "Add multi-language support"
    ],
    "Account": [
        "Want to upgrade my plan",
        "Cancel my subscription",
        "Change registered email",
        "Deactivate my account"
    ]
}

PRIORITY_MAP = {
    "Billing": ["High", "Critical"],
    "Bug": ["High", "Critical"],
    "Login": ["Medium", "High"],
    "Account": ["Low", "Medium"],
    "Feature Request": ["Low"]
}

CHANNELS = ["email", "chat", "web"]
PLANS = ["Free", "Pro", "Enterprise"]


def generate_ticket(ticket_id: int, category: str) -> dict:
    subject = random.choice(CATEGORIES[category])
    description = (
        f"{subject}. This issue is impacting my work and needs resolution. "
        f"Please look into this as soon as possible."
    )

    priority = random.choice(PRIORITY_MAP[category])
    channel = random.choice(CHANNELS)
    plan = random.choice(PLANS)

    created_at = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23)
    )

    sla_breached = 1 if priority == "Critical" and random.random() < 0.6 else 0
    escalated = 1 if sla_breached and plan == "Enterprise" else 0

    return {
        "ticket_id": ticket_id,
        "subject": subject,
        "description": description,
        "channel": channel,
        "category": category,
        "priority": priority,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "customer_plan": plan,
        "sla_breached": sla_breached,
        "escalated": escalated
    }


def generate_dataset(num_tickets: int) -> pd.DataFrame:
    tickets = []
    categories = list(CATEGORIES.keys())

    tickets_per_category = num_tickets // len(categories)
    ticket_id = 1

    for category in categories:
        for _ in range(tickets_per_category):
            tickets.append(generate_ticket(ticket_id, category))
            ticket_id += 1

    return pd.DataFrame(tickets)


if __name__ == "__main__":
    df = generate_dataset(NUM_TICKETS)
    output_path = "data/raw/tickets.csv"
    df.to_csv(output_path, index=False)
    print(f" Synthetic dataset created: {output_path}")
    print(df["category"].value_counts())
