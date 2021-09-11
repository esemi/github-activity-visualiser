import datetime
import logging
import os
import shutil
import subprocess
from typing import List

import click
from github import Github, Repository


def load_user_repos(user_name: str, secret_token: str) -> List[Repository.Repository]:
    logging.info('start load user repos %s', user_name)
    g = Github(secret_token)
    user = g.get_user(user_name)
    assert user.name

    repos = [r for r in user.get_repos()
             if not r.fork and not r.private]
    logging.info('found %d public repos for %s', len(repos), user.name)
    return repos


def clone_and_fetch_log(tmp_dir: str, data_dir: str, repos: List[Repository.Repository]) -> List[str]:
    logfiles = []
    for repo in repos:
        logging.info('clone %s', repo)

        try:
            shutil.rmtree(tmp_dir)
        except FileNotFoundError:
            pass
        cmd_clone = "git clone %s %s" % (repo.clone_url, tmp_dir)
        process = subprocess.run(cmd_clone, shell=True)
        logging.debug('%s %s' % (cmd_clone, process.returncode))
        assert process.returncode == 0

        filename = os.path.join(data_dir, '%s.log' % repo.name)
        cmd_gen = "gource --output-custom-log %s %s" % (filename, tmp_dir)
        process = subprocess.run(cmd_gen, shell=True)
        logging.debug('%s %s' % (cmd_gen, process.returncode))

        if process.returncode != 0:
            logging.warning('gource fetch log incomplete %s', process.returncode)
            continue

        logfiles.append(filename)

    try:
        shutil.rmtree(tmp_dir)
    except FileNotFoundError:
        pass
    logging.info('complete parsed %d repos', len(logfiles))
    return logfiles


def combine_log(data_dir: str, log_files: List[str], history_days: int) -> str:
    current_date = str(datetime.date.today()).replace(' ', '_')
    tmp_log_file = os.path.join(data_dir, 'gource_tmp_%s.log' % current_date)
    final_log_file = os.path.join(data_dir, 'gource_final_%s.log' % current_date)

    for filename in {final_log_file, tmp_log_file}:
        try:
            os.remove(filename)
        except FileNotFoundError:
            continue

    for repo_filepath in log_files:
        logging.info('prepare log %s', repo_filepath)
        project = repo_filepath.split('/')[1][:-4]
        logging.debug('project name %s', project)

        cmd_sed = 'sed -r "s#(.+)|#\\1|/%s#" %s >> %s' % (project, repo_filepath, tmp_log_file)
        process = subprocess.run(cmd_sed, shell=True)
        logging.debug('%s %s' % (cmd_sed, process.returncode))

    # filter logs
    timestamp_border = int((datetime.datetime.utcnow() - datetime.timedelta(days=history_days)).timestamp())
    cmd = "cat %s | awk '$1 > %d {print $0;}' | sort -n > %s" % (
        tmp_log_file,
        timestamp_border,
        final_log_file,
    )
    logging.info('filter logs %s' % cmd)
    process = subprocess.run(cmd, shell=True)
    logging.debug('%s %s' % (cmd, process.returncode))
    return final_log_file


@click.command()
@click.argument('user_name', required=True)
@click.argument('github_token', required=True)
@click.option('--count', default=3, help='Limit of repos.')
@click.option('--history_days', default=365)
@click.option('--data_dir', default='user_logs')
@click.option('--tmp_dir', default='tmp_repo')
@click.option('--verbose', is_flag=True)
def cli(user_name: str, github_token: str, count: int, verbose: bool, data_dir: str, tmp_dir: str, history_days: int):
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG if verbose else logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        user_repos = load_user_repos(user_name, github_token)
    except Exception as e:
        logging.exception(e)
        return

    log_files = clone_and_fetch_log(tmp_dir, data_dir, user_repos[:count])

    if not log_files:
        logging.warning('not found user repos for vis (sic!)')
        return

    final_log = combine_log(data_dir, log_files, history_days)

    subprocess.run(f'gource -s 1 -e 0.005 --title "{history_days} days of {user_name} development" '
                   f'--follow-user {user_name} {final_log}', shell=True)


if __name__ == '__main__':
    cli()
