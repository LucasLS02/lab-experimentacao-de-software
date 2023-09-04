from time import time

from utils.find_age import calculate_age
from utils.paginate_query import async_paginated_query, paginated_query
from utils.save_on_csv import save_on_csv

today = time()


def lab_1_search():
    start_time = time()

    query = '''
            {
                search(query: "stars:>100", type: REPOSITORY, first: 50, after: null) {
                    nodes {
                        ... on Repository {
                            id
                            nameWithOwner
                            url
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

    response_data = paginated_query(query=query, data_amount=1000, page_size=50)

    final_data = []

    for repository in response_data:
        final_data.append({
            'id': repository['id'],
            'nameWithOwner': repository['nameWithOwner'],
            'url': repository['url'],
            'createdAt': repository['createdAt'],
            'updatedAt': repository['updatedAt'],
            'primaryLanguage': repository['primaryLanguage']['name'] if repository['primaryLanguage'] else None,
            'releases': repository['releases']['totalCount'],
            'pullRequests': repository['pullRequests']['totalCount'],
            'issues': repository['issues']['totalCount'],
            'IssuesClosed': repository['IssuesClosed']['totalCount'],
            'age': calculate_age(repository['createdAt']),
            'timeSinceLastUpdate': calculate_age(repository['updatedAt']),
            'reasonIssuesIssuesClosed': repository['IssuesClosed']['totalCount'] / repository['issues']['totalCount'] if
            repository['issues']['totalCount'] > 0 else 0
        })

    save_on_csv(data=final_data, csv_filename=f'{__name__}_data')

    end_time = time()

    print(f'Tempo de duração: {round(end_time - start_time, 2)} segundos.')


async def async_lab_1_search(data_amount=1000, page_size=25):
    start_time = time()

    query = '''
            {
                search(query: "stars:>100", type: REPOSITORY, first: null, after: null) {
                    nodes {
                        ... on Repository {
                            id
                            nameWithOwner
                            url
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

    query = query.replace('first: null', f'first: {page_size}')

    response_data = await async_paginated_query(query=query, data_amount=data_amount, page_size=page_size)

    response_data = response_data['data']['search']['nodes']

    final_data = []

    for repository in response_data:
        final_data.append({
            **repository,
            'age': calculate_age(repository['createdAt']),
            'timeSinceLastUpdate': calculate_age(repository['updatedAt']),
            'reasonIssuesIssuesClosed': repository['issues']['totalCount'] / repository['IssuesClosed']['totalCount'] if
            repository['IssuesClosed']['totalCount'] > 0 else 0
        })

    save_on_csv(data=final_data, csv_filename=f'{__name__}_data')

    end_time = time()

    print(f'Tempo de duração: {round(end_time - start_time, 2)} segundos.')
