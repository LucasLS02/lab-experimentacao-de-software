from utils.async_utils import create_async_task, get_async_tasks_results
from utils.cursor_generator import generate_cursor
from utils.request import async_request, request


def paginated_query(query, data_amount=100, page_size=50):
    response_data = []

    cursor = None
    has_next_page = True

    # for index in range(0, data_amount, page_size):
    while len(response_data) < data_amount or not has_next_page:
        # cursor = generate_cursor(index)

        if cursor is None:
            query_copy = query.replace('after: null', '')
        else:
            query_copy = query.replace('after: null', f'after: "{cursor}"')

        data = {
            'query': query_copy
        }

        response = request(data)

        cursor = response['data']['search']['pageInfo']['endCursor']
        has_next_page = response['data']['search']['pageInfo']['hasNextPage']

        while not isinstance(response, list):
            key = list(response.keys())[0]
            response = response[key]

        response_data.extend(response)

    return response_data


async def async_paginated_query(query, data_amount=100, page_size=50):
    queries = []

    for index in range(0, data_amount, page_size):
        cursor = generate_cursor(index)

        query_copy = query.replace('after: null', f'after: "{cursor}"')

        queries.append({
            'query': query_copy
        })

    tasks = [create_async_task(async_request, query) for query in queries]
    responses = await get_async_tasks_results(tasks)

    final_data = {}

    for response_data in responses:
        final_data.update(response_data)

    return final_data
