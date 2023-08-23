from utils.cursor_generator import generate_cursor
from utils.request import request


def paginated_query(query, data_amount=100, page_size=50):
    response_data = []

    for index in range(0, data_amount + 1, page_size):
        cursor = generate_cursor(index)

        query_copy = query.replace('after: {}', f'after: "{cursor}"')

        data = {
            'query': query_copy
        }

        response = request(data)

        while not isinstance(response, list):
            key = list(response.keys())[0]
            response = response[key]

        response_data.extend(response)

    return response_data
