# Laboratório de Experimentação de Software

## Sprint 1

Para esse sprint, necessitamos de minerar a API do Github (A versão GraphQL) para obter as seguintes informações:

- Com relação aos sistemas com mais estrelas, ou seja, populares, devemos coletar as seguintes informações para serem
  analisadas:
    - Idade dos repositórios (Created at)
    - Total de pull requests aceitas
    - Total de releases
    - Tempo desde a última atualização (Updated at)
    - Linguagem primária
    - Total de issues
    - Total de issues fechadas

Query:

```graphql
 query {
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
```
