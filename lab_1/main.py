from os import environ

from dotenv import load_dotenv
from requests import post

load_dotenv()

query = '''
{
  viewer {
    repositories(first: 10) {
      edges {
        node {
          name
          description
          url
        }
      }
    }
  }
}
'''

payload = {
    'query': query
}

headers = {
    'Authorization': f'bearer {environ["GITHUB_ACCESS_TOKEN"]}'
}

response = post(url=environ['GITHUB_GRAPHQL_ENDPOINT'], json=payload, headers=headers)

response_data = response.json()

print(response_data)
