from uuid import uuid4

from git import Repo


class CloneService:
    def clone_repository(
            self,
            url: str,
            main_as_default_branch=True,
            repo_name: str = None
    ) -> str:
        # default_branch = 'main' if main_as_default_branch else 'master'
        repo_name = repo_name if repo_name else str(uuid4())
        directory_path = f'resources/clone_repos/{repo_name}'
        # command = f'''
        #     git clone \
        #         --quiet --no-tags \
        #         --branch {{default_branch}} --single-branch \
        #         --depth=1 {url} {directory_path}
        # '''
        # formatted_command = command.format_map({'default_branch': default_branch})
        # run(formatted_command, shell=True, check=True)

        Repo.clone_from(url=url, to_path=directory_path,
                        multi_options=['--quiet', '--no-tags', '--single-branch', '--depth=1'])
        return directory_path
