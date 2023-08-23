from os import environ

from requests import post


def request(graphql_query):
    response = post(
        url=environ['GITHUB_GRAPHQL_ENDPOINT'],
        headers={'Authorization': f'bearer {environ["GITHUB_ACCESS_TOKEN"]}'},
        json=graphql_query,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None
