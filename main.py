from multiprocessing import Process
from pathlib import Path
from time import sleep

import pandas as pd
from dotenv import load_dotenv
from numpy import median
from pandas import read_csv

from lab_2.main import lab_2_search
from utils.process_utils import create_queue, create_listener_process, clone_queue_service_wrapper, \
    ck_queue_service_wrapper

# Load .env variables to be used on the functions and componentes.
load_dotenv()

# Lab 1 process

# lab_1_search()

# Lab 2 process

lab_2_search()

clone_queue = create_queue()
ck_queue = create_queue()

csv_path = Path('data/lab_2.main_data.csv')

data_persistance_repo = read_csv(csv_path)

for index, row in data_persistance_repo.iterrows():
    repo_id = row.get('id')
    repo_url = row.get('url')

    clone_queue.put((repo_id, repo_url))

ps: list[Process] = []

for _ in range(2):
    p = create_listener_process(clone_queue_service_wrapper, clone_queue, ck_queue)
    p.start()
    ps.append(p)
for _ in range(3):
    p = create_listener_process(ck_queue_service_wrapper, ck_queue)
    p.start()
    ps.append(p)

all_process_are_dead = False
while not all_process_are_dead:
    qtd_of_process_dead = 0
    for p in ps:
        if not p.is_alive() or (clone_queue.empty() and ck_queue.empty()):
            qtd_of_process_dead += 1
    all_process_are_dead = qtd_of_process_dead == 5

sleep(15)

for index, row in data_persistance_repo.iterrows():
    repo_id = row.get('id')

    repo_data_analysis = pd.read_csv(f'resources/repo_anaylisis/{repo_id}/class.csv')

    cbo = []
    dit = []
    lcom = []
    loc = []

    for index_, repo_data_row in repo_data_analysis.iterrows():
        cbo.append(repo_data_row.get('cbo'))
        dit.append(repo_data_row.get('dit'))
        lcom.append(repo_data_row.get('lcom'))
        loc.append(repo_data_row.get('loc'))

    data_persistance_repo.loc[index, 'cbo'] = median(cbo)
    data_persistance_repo.loc[index, 'dit'] = median(dit)
    data_persistance_repo.loc[index, 'lcom'] = median(lcom)
    data_persistance_repo.loc[index, 'loc'] = median(loc)

    print({
        'cbo': cbo,
        'dit': dit,
        'lcom': lcom,
        'loc': loc
    })

data_persistance_repo.to_csv(csv_path, index=False)
