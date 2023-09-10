from datetime import datetime


def calculate_days(date):
    """
    Calculates the age of a repository
    :param date: date of creation ou update
    :return: age: age of repository
    """
    normalized_age = datetime.utcnow() - datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

    age = normalized_age.days

    return age

def calculate_hours(date):
    """
    Calculates the age of a repository
    :param date: date of creation ou update
    :return: age: age of repository
    """
    normalized_age = datetime.utcnow() - datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

    age = normalized_age.seconds/3600

    return age
