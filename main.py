#!/usr/bin/env python3

import datetime
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
        logging.debug('%s %s' % (cmd_clone, process.returncode))
        assert process.returncode == 0

        filename = os.path.join(settings.DATA_FOLDER, '%s.log' % repo.name)
        cmd_gen = "gource --output-custom-log %s %s" % (filename, settings.REPO_TMP_FOLDER)
        process = subprocess.run(cmd_gen, shell=True)
        logging.debug('%s %s' % (cmd_gen, process.returncode))

        if process.returncode != 0:
            logging.warning('gource fetch log incomplete %s', process.returncode)
            continue

        logfiles.append(filename)

    try:
        shutil.rmtree(settings.REPO_TMP_FOLDER)
    except FileNotFoundError:
        pass
    logging.info('complete parsed %d repos', len(logfiles))
    return logfiles


def combine_log(log_files: list) -> str:
    current_date = str(datetime.date.today()).replace(' ', '_')
    tmp_log_file = os.path.join(settings.DATA_FOLDER, 'gource_tmp_%s.log' % current_date)
    final_log_file = os.path.join(settings.DATA_FOLDER, 'gource_final_%s.log' % current_date)

    for filename in {final_log_file, tmp_log_file}:
        try:
            os.remove(filename)
        except FileNotFoundError:
            continue

    for repo_filepath in log_files:
        logging.info('prepare log %s', repo_filepath)
        project = repo_filepath.split('/')[1][:-4]
        logging.debug('project name %s', project)

        cmd_sed = "sed -r 's#(.+)\|#\\1|/%s#' %s >> %s" % (project, repo_filepath, tmp_log_file)
        process = subprocess.run(cmd_sed, shell=True)
        logging.debug('%s %s' % (cmd_sed, process.returncode))

    # filter logs
    cmd = "cat %s | awk '$1 > %d {print $0;}' | sort -n > %s" % (tmp_log_file, settings.TIMESTAMP_BORDER, final_log_file)
    logging.info('filter logs %s' % cmd)
    process = subprocess.run(cmd, shell=True)
    logging.debug('%s %s' % (cmd, process.returncode))
    return final_log_file


def main(user_login: str):
    try:
        user_repos, user_name = load_user_repos(user_login)
    except Exception as e:
        logging.exception(e)
        return

    log_files = clone_and_fetch_log(user_repos[:3])

    if not log_files:
        logging.warning('not found user repos for vis (sic!)')
        return

    final_log = combine_log(log_files)

    # todo filtering logs (by username) ?

    # todo visualise

    subprocess.run('gource -s 1 -e 0.005 --title "One year of %s development" --follow-user %s %s' %
                   (user_name, user_name, final_log), shell=True)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG if settings.DEBUG else logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')
    assert len(sys.argv) > 1
    main(sys.argv[1])
