import git
import os
import subprocess
import shutil
from logger import logger
from config import BACKEND_DEV_SERVICE, BACKEND_PROJECT_DIR, \
    BACKEND_REPO_URL, BACKEND_TEST_SERVICE, DEV_BRANCH, \
    TEST_BRANCH


def prepare(tag):
    logger.debug("start clone")
    repo = git.Repo.clone_from(
        url=BACKEND_REPO_URL, to_path=BACKEND_PROJECT_DIR)
    repo.git.checkout(tag)
    logger.debug("pull over.")
    shutil.rmtree(os.path.join(BACKEND_PROJECT_DIR, '.git'))


def build(target):
    logger.debug("start build...")
    os.chdir(BACKEND_PROJECT_DIR)
    subprocess.call(
        f"/home/alex/workspace/install/apache-maven-3.8.1/bin/mvn clean package", shell=True)
    subprocess.call(
        f'docker-compose stop {target} && docker-compose rm -f {target}', shell=True)
    subprocess.call(
        f'docker rmi solstreet-be_{target}', shell=True)
    subprocess.call(
        f'docker-compose -f {BACKEND_PROJECT_DIR}/docker-compose.yaml up --build -d {target}', shell=True)


def clean():
    for filename in os.listdir(BACKEND_PROJECT_DIR):
        file_path = os.path.join(BACKEND_PROJECT_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error('Failed to delete %s. Reason: %s' % (file_path, e))


def deploy_be(tag, branch):
    try:
        clean()
        prepare(tag)
        if branch.startswith(DEV_BRANCH):
            logger.debug('start deploy backend dev')
            build(BACKEND_DEV_SERVICE)
        elif branch.startswith(TEST_BRANCH):
            logger.debug('start deploy backend test')
            build(BACKEND_TEST_SERVICE)
        else:
            logger.debug(f'ignore branch ==> {branch}')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    deploy_be('v0.0.5',  DEV_BRANCH)
