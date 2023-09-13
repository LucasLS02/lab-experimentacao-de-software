import os
from subprocess import run


class CodeMetricAnalyserService:
    def analyse_project(self, project_path: str):

        repo_name = project_path.split('/')[2]

        try:
            analysis_result_path = f'resources/repo_anaylisis/{repo_name}/'
            os.mkdir(analysis_result_path)
            run(f'java -jar ck.jar {project_path} false 0 False {analysis_result_path}', shell=True, check=True)
            return analysis_result_path
        except Exception as e:
            print(e)
            raise e
