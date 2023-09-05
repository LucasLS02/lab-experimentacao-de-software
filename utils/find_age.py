from datetime import datetime


def calculate_age(date):
    """
    Calculates the age of a repository
    :param date: date of creation ou update
    :return: age: age of repository
    """
    normalized_age = datetime.utcnow() - datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

    age = normalized_age.days

    return age
