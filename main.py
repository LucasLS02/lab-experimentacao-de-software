from time import time

from dotenv import load_dotenv
from numpy import median, sum
from pandas import read_csv

from lab_2.main import lab_2_search
from lab_3.main import lab_3_search
from utils.process_utils import create_queue, create_listener_process, clone_queue_service_wrapper, \
    ck_queue_service_wrapper

load_dotenv()

# Lab 2 process

# print('---------------------------------------------------------')
# print('Start getting repos')
# print('---------------------------------------------------------')

# start_lab_2 = time()

# start_get_repos = time()

# original_csv_path = lab_2_search()

# csv_path = original_csv_path.absolute()

# csv_path = str(csv_path).replace('.csv', '')

# df = read_csv(original_csv_path)

# # Divida o DataFrame ao meio
# tamanho = len(df)
# metade = tamanho // 2
# parte1 = df.iloc[:metade]
# parte2 = df.iloc[metade:]

# nome_arquivo_saida1 = f'{csv_path}_part_1.csv'
# parte1.to_csv(nome_arquivo_saida1, index=False)

# nome_arquivo_saida2 = f'{csv_path}_part_2.csv'
# parte2.to_csv(nome_arquivo_saida2, index=False)

# end_get_repos = time()

# print('---------------------------------------------------------')
# print('End getting repos')
# print('---------------------------------------------------------')

# for csv_path in [nome_arquivo_saida1, nome_arquivo_saida2]:
#     print('---------------------------------------------------------')
#     print('Start cloning repos')
#     print('---------------------------------------------------------')

#     start_cloning__data = time()

#     clone_queue = create_queue()
#     ck_queue = create_queue()

#     data_persistence_repo = read_csv(csv_path)

#     number_of_process = 7

#     for index, row in data_persistence_repo.iterrows():
#         repo_id = row.get('local_id')
#         repo_url = row.get('url')

#         clone_queue.put((repo_id, repo_url))

#     for _ in range(number_of_process):
#         clone_queue.put(None)

#     cloned_repos_process = []

#     time_execution_clone = 0
#     time_execution_analysis = 0

#     for index in range(number_of_process):
#         process_clone = create_listener_process(clone_queue_service_wrapper, clone_queue, ck_queue)

#         process_clone.start()

#         cloned_repos_process.append(process_clone)

#     is_running = True
#     retries = 0

#     while is_running:
#         if clone_queue.empty():
#             retries += 1

#         if retries == (2 * number_of_process):
#             is_running = False
#             break

#     end_cloning_repo = time()

#     time_execution_clone += (end_cloning_repo - start_cloning__data)

#     print('---------------------------------------------------------')
#     print('Finish cloning repos')
#     print('---------------------------------------------------------')

#     print('---------------------------------------------------------')
#     print('Start analysing repos')
#     print('---------------------------------------------------------')

#     start_analysing_repo = time()

#     analysis_repos_process = []

#     for _ in range(number_of_process):
#         ck_queue.put(None)

#     for index in range(number_of_process):
#         process_analysis = create_listener_process(ck_queue_service_wrapper, ck_queue)

#         process_analysis.start()

#         analysis_repos_process.append(process_analysis)

#     is_running = True
#     retries = 0

#     while is_running:
#         if ck_queue.empty():
#             retries += 1

#         if retries == (2 * number_of_process):
#             is_running = False
#             break

#     end__analysing_repo = time()

#     time_execution_analysis += (end__analysing_repo - start_analysing_repo)

#     print('---------------------------------------------------------')
#     print('Finish analysing repos')
#     print('---------------------------------------------------------')

# print('---------------------------------------------------------')
# print('Start updating CSV')
# print('---------------------------------------------------------')

# start_updating_csv = time()

# data_persistence_repo = read_csv(original_csv_path)

# for index, row in data_persistence_repo.iterrows():
#     repo_id = row.get('local_id')

#     print(f'resources/repo_anaylisis/{repo_id}/class.csv')

#     try:

#         repo_data_analysis = read_csv(f'resources/repo_anaylisis/{repo_id}/class.csv')

#         if not repo_data_analysis.empty:
#             print('atualizado')
#             print('')

#             cbo = []
#             dit = []
#             lcom = []
#             loc = []

#             for index_, repo_data_row in repo_data_analysis.iterrows():
#                 cbo.append(repo_data_row.get('cbo'))
#                 dit.append(repo_data_row.get('dit'))
#                 lcom.append(repo_data_row.get('lcom'))
#                 loc.append(repo_data_row.get('loc'))

#             data_persistence_repo.loc[index, 'cbo'] = median(cbo) if len(cbo) > 0 else 0
#             data_persistence_repo.loc[index, 'dit'] = max(dit) if len(dit) > 0 else 0
#             data_persistence_repo.loc[index, 'lcom'] = median(lcom) if len(lcom) > 0 else 0
#             data_persistence_repo.loc[index, 'loc'] = sum(loc) if len(loc) > 0 else 0
#         else:
#             print('não atualizado')

#     except Exception as e:
#         print(e)

# print(data_persistence_repo)

# data_persistence_repo.to_csv('./data/lab_2.main_data_final.csv', index=False)

# end_updating_csv = time()

# print('---------------------------------------------------------')
# print('Endpoint updating CSV')
# print('---------------------------------------------------------')

# end_lab_2 = time()

# time_execution_lab_2 = f'{round((end_lab_2 - start_lab_2) / 60, 2)} minutos'

# print('---------------------------------------------------------')
# print('Estatísticas do lab 2')
# print('---------------------------------------------------------')
# print('')
# print(
#     f'Tempo para buscar repositórios (API Graphql github): {round((end_get_repos - start_get_repos) / 60, 2)} minutos')
# print(f'Tempo para clonar os repositórios: {round(time_execution_clone / 60, 2)} minutos')
# print(
#     f'Tempo para clonar os repositórios: {round(time_execution_analysis / 60, 2)} minutos')
# print(f'Tempo para atualizar dados CSV: {round((end_updating_csv - start_updating_csv) / 60, 2)} minutos')
# print(f'Tempo de execução total: {time_execution_lab_2}')
# print('')
# print('---------------------------------------------------------')

# Lab 3 process

lab_3_search()
