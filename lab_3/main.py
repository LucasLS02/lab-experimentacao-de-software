import pandas as pd
import base64
from time import sleep
from os.path import exists
from pathlib import Path
from time import time
from utils.paginate_query import paginated_query
from utils.save_on_csv import save_on_csv
from utils.request import request_graphQl_api

from datetime import datetime


def lab_3_search():
    if not exists(f'data/{__name__}_data_repository.csv'):
        start_time = time()

        query = '''
            {
                search(query: "stars:>100", type: REPOSITORY, first: 100, after: null) {
                    nodes {
                    ... on Repository {
                        id
                        nameWithOwner
                        pullRequests{
                        totalCount
                        }
                    }
                    }
                    pageInfo {
                    endCursor
                    hasNextPage
                    }
                }
            }
        '''

        response_data = paginated_query(query=query, data_amount=200, page_size=100)

        final_data = []
        total_pull_requests = 0

        for data in response_data:
            final_data.append({
                'id': data['id'],
                'nameWithOwner': data['nameWithOwner'],
                'pullRequests': data['pullRequests']['totalCount']
            })
            total_pull_requests += data['pullRequests']['totalCount']

        save_on_csv(data=final_data, csv_filename=f'{__name__}_data_repository')

        print('')
        print(f'Total de pull requests: {total_pull_requests}')
        print('')

        end_time = time()

        print(f'Tempo de duração coleta dos repositórios: {round(end_time - start_time, 2)} segundos.')

    if not exists(f'data/{__name__}_data_repository_prs.csv'):
        start_time = time()
        repos_data = pd.read_csv(f'data/{__name__}_data_repository.csv')

        for index, row in repos_data.iterrows():
            current_repo = {
                'current_repo': row.get('nameWithOwner'),
                'index': index
            }

            save_on_csv(csv_filename=f'{__name__}_current_repo', data=[current_repo])

            print('')
            print(f'Faltam {len(repos_data) - index} repositórios para coletar as PR`s.')
            print('')
            owner, name = row.get('nameWithOwner').split('/')

            query_prs = '''{
                repository(owner: "nome-do-proprietario", name: "nome-do-repositorio") {
                    pullRequests(first: 100, after: null, states: [MERGED, CLOSED]) {
                    nodes {
                        author {
                        login
                        }
                        body
                        changedFiles
                        closed
                        closedAt
                        createdAt
                        deletions
                        id
                        lastEditedAt
                        merged
                        mergedAt
                        number
                        state
                        title
                        reviews {
                        totalCount
                        }
                    }
                    pageInfo {
                        endCursor
                        hasNextPage
                    }
                    }
                }
                }
            '''

            query_prs = query_prs.replace('nome-do-proprietario', owner)
            query_prs = query_prs.replace('nome-do-repositorio', name)

            cursor = None
            has_next_page = True

            response_data = []

            while has_next_page:
                if cursor is None:
                    query_copy = query_prs.replace('after: null', '')
                else:
                    query_copy = query_prs.replace('after: null', f'after: "{cursor}"')

                data = {
                    'query': query_copy
                }

                sleep(2)

                try:
                    response = request_graphQl_api(data)
                except Exception as e:
                    sleep(60)
                    response = request_graphQl_api(data)

                if response is None:
                    cursor = None
                    has_next_page = False
                    print('Has next page: False')
                else:

                    now = datetime.now()
                    print(f'Has next page: {response['data']['repository']['pullRequests']['pageInfo']['hasNextPage'] if ('data' in response and response['data']['repository']['pullRequests']['pageInfo']['hasNextPage']) else False} | {now}')
                    has_next_page = False
                    
                    cursor = response['data']['repository']['pullRequests']['pageInfo']['endCursor'] if ('data' in response and response['data']['repository']['pullRequests']['pageInfo']['hasNextPage']) else None
                    has_next_page = response['data']['repository']['pullRequests']['pageInfo']['hasNextPage'] if ('data' in response and response['data']['repository']['pullRequests']['pageInfo']['hasNextPage']) else False

                    while not isinstance(response, list):
                        key = list(response.keys())[0]
                        response = response[key]

                    response_data.extend(response)

                    final_data = []

                    for data in response_data:
                        sample_string_bytes = data['body'].encode() 
                        
                        base64_bytes = base64.b64encode(sample_string_bytes) 
                        base64_string = base64_bytes.decode() 

                        final_data.append({
                            'author': data['author']['login'] if data['author'] is not None else None,
                            'body': base64_string,
                            'bodySize': len(data['body']),
                            'changedFiles': data['changedFiles'],
                            'closed': data['closed'],
                            'closedAt': data['closedAt'],
                            'createdAt': data['createdAt'],
                            'deletions': data['deletions'],
                            'id': data['id'],
                            'lastEditedAt': data['lastEditedAt'],
                            'merged': data['merged'],
                            'mergedAt': data['mergedAt'],
                            'number': data['number'],
                            'state': data['state'],
                            'title': data['title'],
                            'reviews': data['reviews']['totalCount']
                        })

                    save_on_csv(data=final_data, csv_filename=f'{__name__}_data_repository_prs')

        final_data = []

        for data in response_data:
            sample_string_bytes = data['body'].encode() 
            
            base64_bytes = base64.b64encode(sample_string_bytes) 
            base64_string = base64_bytes.decode() 

            final_data.append({
                'author': data['author']['login'] if data['author'] is not None else None,
                'body': base64_string,
                'bodySize': len(data['body']),
                'changedFiles': data['changedFiles'],
                'closed': data['closed'],
                'closedAt': data['closedAt'],
                'createdAt': data['createdAt'],
                'deletions': data['deletions'],
                'id': data['id'],
                'lastEditedAt': data['lastEditedAt'],
                'merged': data['merged'],
                'mergedAt': data['mergedAt'],
                'number': data['number'],
                'state': data['state'],
                'title': data['title'],
                'reviews': data['reviews']['totalCount']
            })

        save_on_csv(data=final_data, csv_filename=f'{__name__}_data_repository_prs')

        end_time = time()

        print(f'Tempo de duração coleta das PR`s dos repositórios: {round(end_time - start_time, 2)} segundos.')

    prs_data = pd.read_csv(f'data/{__name__}_data_repository_prs.csv')

    valid_data = []

    for index, data in prs_data.iterrows():
        if isinstance(data['createdAt'], str) and isinstance(data['closedAt'], str):
            start_time = datetime.fromisoformat(data['createdAt'].replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(data['closedAt'].replace("Z", "+00:00"))

            has_more_than_one_hour = (end_time - start_time).seconds > 3600

            if (data.get('closed') or data.get('merged')) and data['reviews'] > 0 and has_more_than_one_hour:
                valid_data.append(data)
    
    print('')
    print(f'Valid data: {len(valid_data)}')
    print('')
    
    save_on_csv(data=valid_data, csv_filename=f'{__name__}_data_repository_prs_valid')

    return Path(f'data/{__name__}_data_user.csv')
