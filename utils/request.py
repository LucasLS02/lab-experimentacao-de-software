import json
from os import environ
from time import sleep
from requests import post


def request_graphQl_api(graphql_query):
    sleep(1)
    response = post(
        url=environ['GITHUB_GRAPHQL_ENDPOINT'],
        headers={'Authorization': f'bearer {environ["GITHUB_ACCESS_TOKEN"]}'},
        json=graphql_query,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


# async def async_request(graphql_query):
#     headers = {'Authorization': f'bearer {environ["GITHUB_ACCESS_TOKEN"]}'}
#     data = json.dumps(graphql_query)
#     async with aiohttp.ClientSession(headers=headers) as session:
#         async with session.post(url=environ['GITHUB_GRAPHQL_ENDPOINT'], data=data) as response:
#             return await response.json()
