from os.path import exists
from pathlib import Path
from time import time
from uuid import uuid4

from utils.find_age import calculate_days
from utils.paginate_query import paginated_query
from utils.save_on_csv import save_on_csv


def lab_2_search():
    if not exists(f'data/{__name__}_data.csv'):
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
                    pageInfo {   # Add this section to get pageInfo
                      endCursor
                      hasNextPage
                    }
                  }
                }
        '''

        response_data = paginated_query(query=query, data_amount=1150, page_size=50)

        unique_data = []
        non_unique_data = []
        final_data = []

        for repository in response_data:
            if repository['nameWithOwner'] not in unique_data:
                unique_data.append(repository['nameWithOwner'])
                final_data.append({
                    'id': repository['id'],
                    'local_id': uuid4(),
                    'nameWithOwner': repository['nameWithOwner'],
                    'url': repository['url'],
                    'createdAt': repository['createdAt'],
                    'stars': repository['stargazerCount'],
                    'releases': repository['releases']['totalCount'],
                    'age': calculate_days(repository['createdAt']) / 365
                })
            else:
                non_unique_data.append(repository['nameWithOwner'])

        save_on_csv(data=final_data, csv_filename=f'{__name__}_data')

        end_time = time()

        print(f'Tempo de duração: {round(end_time - start_time, 2)} segundos.')

    return Path(f'data/{__name__}_data.csv')
