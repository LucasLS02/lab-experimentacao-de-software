from time import time

from utils.paginate_query import paginated_query
from utils.save_on_csv import save_on_csv


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

    save_on_csv(data=response_data, csv_filename=f'{__name__}_data')

    end_time = time()

    print(f'Tempo de duração: {round(end_time - start_time, 2)} segundos.')
