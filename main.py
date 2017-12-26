import logging
import subprocess
import os
import shutil

import sys
from github import Github

import settings


def load_user_repos(user: str) -> list:
    logging.info('start load user repos %s', user)
    g = Github(settings.GITHUB_TOKEN)
    repos = [r for r in g.get_user(user).get_repos()
             if not r.fork and not r.private]
    logging.info('found %d public repos', len(repos))
    return repos


def clone_and_fetch_log(repos: list):
    for repo in repos:
        logging.info('process %s repo', repo)

        try:
            shutil.rmtree(settings.REPO_TMP_FOLDER)
        except FileNotFoundError:
            pass
        cmd_clone = "git clone %s %s" % (repo.clone_url, settings.REPO_TMP_FOLDER)
        process = subprocess.run(cmd_clone, shell=True)
        logging.debug('%s %s %s' % (cmd_clone, process.returncode, process.stderr))
        assert process.returncode == 0

        cmd_gen = "gource --output-custom-log %s %s" % (repo.name, settings.REPO_TMP_FOLDER)
        process = subprocess.run(cmd_gen, shell=True)
        logging.debug('%s %s %s' % (cmd_gen, process.returncode, process.stderr))


def main(user_login: str):
    user_repos = load_user_repos(user_login)
    if not user_repos:
        logging.info('not found user repos')
        return

    # todo clone repos and gen logs
    log_files = clone_and_fetch_log(user_repos)

    # todo filtering logs (by year and user)

    # todo visualise


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG if settings.DEBUG else logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    # assert len(sys.argv) > 1
    main('gritzko')
