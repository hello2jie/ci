import git
import os
import subprocess
import shutil
from logger import logger
from config import WEB_REPO_URL, WEB_PROJECT_DIR, WEB_DEV_SERVICE, \
    WEB_TEST_SERVICE, TEST_BRANCH, DEV_BRANCH, DEV_CONFIG, TEST_CONFIG


def prepare(tag):
    logger.debug("start clone")
    repo = git.Repo.clone_from(url=WEB_REPO_URL, to_path=WEB_PROJECT_DIR)
    repo.git.checkout(tag)
    logger.debug("pull over.")
    shutil.rmtree(os.path.join(WEB_PROJECT_DIR, '.git'))


def build(target, config_file):
    logger.debug("start build...")
    os.chdir(WEB_PROJECT_DIR)
    CONFIG_PATH = os.path.join(WEB_PROJECT_DIR, 'src//config')
    subprocess.call(
        f"cp {os.path.join(CONFIG_PATH, config_file)} {os.path.join(CONFIG_PATH, 'config.ts')}", shell=True)
    subprocess.call(
        f"npm install && npm run build", shell=True)
    subprocess.call(
        f'docker-compose stop {target} && docker-compose rm -f {target}', shell=True)
    subprocess.call(
        f'docker rmi solstreet-fe_{target}', shell=True)
    subprocess.call(
        f'docker-compose -f {WEB_PROJECT_DIR}/docker-compose.yaml up --build -d {target}', shell=True)


def clean():
    for filename in os.listdir(WEB_PROJECT_DIR):
        file_path = os.path.join(WEB_PROJECT_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error('Failed to delete %s. Reason: %s' % (file_path, e))


def deploy_fe(tag, branch):
    try:
        clean()
        prepare(tag)
        if DEV_BRANCH in branch:
            logger.debug('start deploy web dev')
            build(WEB_DEV_SERVICE, DEV_CONFIG)
        elif TEST_BRANCH in branch:
            logger.debug('start deploy web test')
            build(WEB_TEST_SERVICE, TEST_CONFIG)
        else:
            logger.debug(f'ignore branch ==> {branch}')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    deploy_fe('v0.0.2', DEV_BRANCH)
