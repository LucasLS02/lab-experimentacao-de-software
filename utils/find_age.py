from datetime import datetime


def calculate_age(created_at):
    created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")

    age = (datetime.utcnow() - created_at).days // 365

    return age
