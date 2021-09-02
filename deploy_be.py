import git
import os
import subprocess
import shutil
from logger import logger

# Repo
REPO_URL = "git@github.com:0xalexbai/solhedge-be.git"
# 项目路径
PROJECT_DIR = '/home/alex/deploy/solhedge-be'
# 编译生成路径
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
BACKEND_TEST_SERVICE = 'backend-test'
BACKEND_DEV_SERVICE = 'backend-dev'


def prepare(tag):
    logger.debug("start clone")
    repo = git.Repo.clone_from(url=REPO_URL, to_path=PROJECT_DIR)
    repo.git.checkout(tag)
    logger.debug("pull over.")


def build(target):
    logger.debug("start build...")
    os.chdir(PROJECT_DIR)
    subprocess.call(
        f"mvn clean package", shell=True)
    subprocess.call(
        f'docker-compose -f {PROJECT_DIR}/docker-compose.yaml up --build -d {target}', shell=True)


def clean():
    if os.path.isdir(PROJECT_DIR):
        shutil.rmtree(PROJECT_DIR)
    os.makedirs(PROJECT_DIR)


def deploy_be(tag, branch):
    try:
        clean()
        prepare(tag)
        if branch == 'refs/heads/dev':
            logger.debug('start deploy backend dev')
            build(BACKEND_DEV_SERVICE)
        elif branch == 'refs/heads/test':
            logger.debug('start deploy backend test')
            build(BACKEND_TEST_SERVICE)
        else:
            logger.debug(f'ignore branch ==> {branch}')
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    deploy_be('v1.0.2', BACKEND_DEV_SERVICE)
