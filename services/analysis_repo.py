import os
from subprocess import run


def ck_analyse_repo(repo_path: str):
    try:
        repo_name = repo_path.split('/')[2]
        analysis_result_path = f'resources/repo_anaylisis/{repo_name}/'

        os.mkdir(analysis_result_path)

        response = run(f'java -jar ck.jar {repo_path} false 0 False {analysis_result_path}', shell=True, check=True)

        return {'repo_analysis_path': analysis_result_path, 'status': response.returncode}

    except Exception as e:
        print(e)
        return None
