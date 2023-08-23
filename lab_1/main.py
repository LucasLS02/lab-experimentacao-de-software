from time import time

from utils.cursor_generator import generate_cursor
from utils.request import request
from utils.save_on_csv import save_on_csv


def lab_1_search():
    start_time = time()

    response_data = []

    for index in range(0, 1001, 50):
        query = '''
        {
              search(query: "stars:>100", type: REPOSITORY, first: 50, after: {}) {
                nodes {
                  ... on Repository {
                    id
                    name
                    createdAt
                    updatedAt
                    primaryLanguage {
                      id
                      name
                    }
                    releases(orderBy: {field: CREATED_AT, direction: DESC}) {
                      totalCount
                    }
                    pullRequests(states: MERGED) {
                      totalCount
                    }
                    issues {
                      totalCount
                    }
                    IssuesClosed: issues(states: CLOSED) {
                      totalCount
                    }
                  }
                }
              }
            }
        '''

        query = query.replace('after: {}', f'after: "{generate_cursor(index)}"')

        data = {
            'query': query
        }

        response = request(data)

        response_data.extend(response['data']['search']['nodes'])

    save_on_csv(response_data, f'{__name__}_data')

    end_time = time()

    print(f'Tempo de duração: {round(end_time - start_time, 2)} segundos.')
