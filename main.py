import logging
import subprocess
import os
import sys
import shutil

from github import Github

import settings


def load_user_repos(user: str) -> (list, str):
    logging.info('start load user repos %s', user)
    g = Github(settings.GITHUB_TOKEN)
    user = g.get_user(user)
    assert user.name

    repos = [r for r in user.get_repos()
             if not r.fork and not r.private]
    logging.info('found %d public repos for %s', len(repos), user.name)
    return repos, user.name


def clone_and_fetch_log(repos: list) -> list:
    logfiles = []
    for repo in repos:
        logging.info('clone %s', repo)

        try:
            shutil.rmtree(settings.REPO_TMP_FOLDER)
        except FileNotFoundError:
            pass
        cmd_clone = "git clone %s %s" % (repo.clone_url, settings.REPO_TMP_FOLDER)
        process = subprocess.run(cmd_clone, shell=True)
        logging.debug('%s %s %s' % (cmd_clone, process.returncode, process.stderr))
        assert process.returncode == 0

        filename = os.path.join(settings.DATA_FOLDER, '%s.log' % repo.name)
        cmd_gen = "gource --output-custom-log %s %s" % (filename, settings.REPO_TMP_FOLDER)
        process = subprocess.run(cmd_gen, shell=True)
        logging.debug('%s %s %s' % (cmd_gen, process.returncode, process.stderr))
        assert process.returncode == 0
        logfiles.append(filename)

    logging.info('cloned %d repos', len(logfiles))
    return logfiles


def main(user_login: str):
    user_repos, user_name = load_user_repos(user_login)
    if not user_repos:
        logging.info('not found user repos')
        return

    log_files = clone_and_fetch_log(user_repos)
    assert len(log_files) == len(user_repos)


    # todo filtering logs (by year and username)

    # todo visualise


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG if settings.DEBUG else logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    # assert len(sys.argv) > 1
    main('gritzko')
