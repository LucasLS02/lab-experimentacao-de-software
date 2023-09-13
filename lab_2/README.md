# Laboratório de Experimentação de Software

## Sprint 1

Neste laboratório, iremos realizar uma análise sobre os top 1000 repositórios da lingaugem 
Java com relação a 4 pontos:

- RQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade? 
- RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade ? 
- RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?  

Com relação a esse sistema, precisaremos coletar as seguintes informações:

- RQ 01:
  - Número de estrelas
  - Coupling between objects (CBO)
  - Depth Inheritance Tree (DIT)
  - Lack of Cohesion of Methods (LCOM)
- RQ 02:
  - Idade (em anos)
  - Coupling between objects (CBO)
  - Depth Inheritance Tree (DIT)
  - Lack of Cohesion of Methods (LCOM)
- RQ 03
  - Número de Releases
  - Coupling between objects (CBO)
  - Depth Inheritance Tree (DIT)
  - Lack of Cohesion of Methods (LCOM)
- RQ 04
  - Linhas de código (LOC)
  - Coupling between objects (CBO)
  - Depth Inheritance Tree (DIT)
  - Lack of Cohesion of Methods (LCOM)

Query:

```graphql
query {
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
```
