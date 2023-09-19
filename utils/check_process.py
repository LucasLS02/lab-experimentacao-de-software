from time import sleep

from utils.process_utils import create_listener_process, clone_queue_service_wrapper, ck_queue_service_wrapper


def check_and_restart_processes(processes: list, params: dict):
    for i, process in enumerate(processes):
        if process.poll() is not None:
            print(f"Processo {i + 1} morreu. Reiniciando...")
            process.end()

            new_process = create_listener_process(params.get('function'), params.get('queue'),
                                                  params.get('deposit_queue'))

            processes[i] = new_process


def are_all_processes_dead(processes):
    for process in processes:
        if process is not None and not process.is_alive():
            return False
    return True


def verify_process(clone_queue, ck_queue, cloned_repos_process, analysis_repos_process, number_of_process):
    sleep(10)
    while not clone_queue.empty() or not ck_queue.empty():
        print('---------------------------------------------------------', flush=True)
        print(f'Processos clone ativos: {len(cloned_repos_process)}', flush=True)
        print(f'Processos analysis ativos: {len(analysis_repos_process)}', flush=True)
        print('---------------------------------------------------------', flush=True)

        if not clone_queue.empty():
            check_and_restart_processes(cloned_repos_process,
                                        {'function': clone_queue_service_wrapper, 'queue': clone_queue,
                                         'deposit_queue': ck_queue})

        if not ck_queue.empty():
            check_and_restart_processes(analysis_repos_process,
                                        {'function': ck_queue_service_wrapper, 'queue': ck_queue})

        if clone_queue.empty() and ck_queue.empty() and len(analysis_repos_process) < 2 * number_of_process:
            for clone_process in cloned_repos_process:
                clone_process.kill() if clone_process.is_alive() else None

            if are_all_processes_dead(cloned_repos_process):
                for _ in range(number_of_process):
                    process_analysis = create_listener_process(ck_queue_service_wrapper, ck_queue)

                    process_analysis.start()

                    analysis_repos_process.append(process_analysis)

                    print('---------------------------------------------------------')
                    print('Processo CK adicionado')
                    print('---------------------------------------------------------')
