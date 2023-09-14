import os


def is_alredy_cloned(repo_name):
    """Check if the repository is already cloned."""
    return os.path.isdir(f'resources/repo_anaylisis/{repo_name}')
