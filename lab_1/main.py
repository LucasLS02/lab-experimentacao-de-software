from os import environ

import pandas as pd
from dotenv import load_dotenv
from requests import post

load_dotenv()

query = """
{
  search(query: "stars:>100", type: REPOSITORY, first: 100) {
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
"""

headers = {
    'Authorization': f'bearer {environ["GITHUB_ACCESS_TOKEN"]}'
}

data = {
    'query': query
}

response = post(environ['GITHUB_GRAPHQL_ENDPOINT'], json=data, headers=headers)

response_data = response.json()

nodes_data = response_data['data']['search']['nodes']

df = pd.DataFrame(nodes_data)

csv_filename = "data.csv"

df.to_csv(csv_filename, index=False)

print('Data acquired and saved to data.csv')
