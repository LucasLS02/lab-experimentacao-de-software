from time import time

from utils.find_age import calculate_days
from utils.paginate_query import paginated_query
from utils.save_on_csv import save_on_csv


def lab_2_search():
    start_time = time()

    query = '''
            {
              search(query: "language:Java", type: REPOSITORY, first: 50, after: null) {
                nodes {
                  ... on Repository {
                    url
                    nameWithOwner
                    id
                    stargazerCount
                    createdAt
                    releases {
                      totalCount
                    }
                  }
                }
              }
            }
    '''

    response_data = paginated_query(query=query, data_amount=1000, page_size=50)

    final_data = []
    repositories_ids = []

    for repository in response_data:
        if repository['id'] not in repositories_ids:
            repositories_ids.append(repository['id'])
            final_data.append({
                'id': repository['id'],
                'nameWithOwner': repository['nameWithOwner'],
                'url': repository['url'],
                'createdAt': repository['createdAt'],
                'stars': repository['stargazerCount'],
                'releases': repository['releases']['totalCount'],
                'age': calculate_days(repository['createdAt']) / 365
            })

    save_on_csv(data=final_data, csv_filename=f'{__name__}_data')

    end_time = time()

    print(f'Tempo de duração: {round(end_time - start_time, 2)} segundos.')
