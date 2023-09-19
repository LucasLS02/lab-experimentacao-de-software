from git import Repo

from utils.verify_cloned_repository import is_alredy_cloned


def clone_repo(repo_id, repo_url):
    try:
        retry = 0
        is_succesfull = False
        directory_path = f'resources/clone_repos/{repo_id}'

        while retry < 10 and not is_succesfull:
            if not is_alredy_cloned(repo_id):
                try:
                    Repo.clone_from(url=repo_url, to_path=directory_path,
                                    multi_options=['--quiet', '--no-tags', '--single-branch', '--depth=1'])

                    is_succesfull = True
                except Exception as e:
                    print(e)
                    retry += 1

            else:
                is_succesfull = True

        if is_succesfull:
            return directory_path

    except Exception as e:
        print(e)
        return None
