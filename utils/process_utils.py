from multiprocessing import Process, Queue
from os import system
from os.path import exists
from queue import Empty
from time import sleep
from typing import Callable

from services.analysis_repo import ck_analyse_repo
from services.clone_repo import clone_repo
from utils.verify_cloned_repository import is_alredy_cloned


class Wrapper:
    def __init__(
            self,
            function: Callable,
            consumer_queue: Queue,
            deposit_queue: Queue
    ):
        self._function = function
        self._consumer_queue = consumer_queue
        self._deposit_queue = deposit_queue

    def run(self):
        should_keep_on_consuming = True
        retries_count = 0
        while should_keep_on_consuming:
            try:
                if retries_count == 5:
                    should_keep_on_consuming = False
                data = self._consumer_queue.get_nowait()
                result = self._function(data)
                if self._deposit_queue and result is not None:
                    self._deposit_queue.put_nowait(result)
            except Empty:
                sleep(1)
                retries_count += 1


def clone_queue_service_wrapper(row_data):
    if row_data is None:
        raise Exception()
    repo_id, repo_url = row_data[0], row_data[1]
    if not is_alredy_cloned(repo_id):
        try:
            directory_path = clone_repo(repo_id, repo_url)

            if directory_path is not None and exists(directory_path):
                print(f'Project cloned: {repo_id}')
                print(f'Project added to analysis queue: {repo_id}')
                return directory_path

            else:
                print('')
                print(f'Error on clone project {repo_id}')
                print('')
                raise Exception()
        except Exception as e:
            print('')
            print(e)
            print('')
            raise Exception()


def create_listener_process(
        function: Callable,
        queue: Queue,
        deposit_queue: Queue = None
):
    process = Process(
        target=Wrapper(function, queue, deposit_queue).run,
        daemon=True
    )
    return process


def ck_queue_service_wrapper(repository_dir):
    if repository_dir is None:
        raise Exception()
    is_successful = False

    while not is_successful:
        response = ck_analyse_repo(repository_dir)

        status = response['status']

        if response is not None and status == 0 and exists(response['repo_analysis_path']):
            system(f'rm -rf {repository_dir}')
            print(f'Project analysed: {repository_dir}')
            is_successful = True
        else:
            print('')
            print(f'Error on analyse project {repository_dir}')
            print('')


def create_queue():
    return Queue()
