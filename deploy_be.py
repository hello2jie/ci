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
BACKEND_TEST_SERVICE = 'solhedge-test-server'
BACKEND_DEV_SERVICE = 'solhedge-dev-server'


def prepare(tag):
    logger.debug("start clone")
    repo = git.Repo.clone_from(url=REPO_URL, to_path=PROJECT_DIR)
    repo.git.checkout(tag)
    logger.debug("pull over.")


def build(target):
    logger.debug("start build...")
    os.chdir(PROJECT_DIR)
    subprocess.call(
        f"/home/alex/workspace/install/apache-maven-3.8.1/bin/mvn clean package", shell=True)
    subprocess.call(
        f'docker-compose stop {target} && docker-compose rm {target}', shell=True)
    subprocess.call(
        f'docker rmi solhedge-be_{target}', shell=True)
    subprocess.call(
        f'docker-compose -f {PROJECT_DIR}/docker-compose.yaml up --build -d {target}', shell=True)


def clean():
    for filename in os.listdir(PROJECT_DIR):
        file_path = os.path.join(PROJECT_DIR, filename)
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
        if branch == 'refs/heads/dev':
            logger.debug('start deploy backend dev')
            build(BACKEND_DEV_SERVICE)
        elif branch == 'refs/heads/test':
            logger.debug('start deploy backend test')
            build(BACKEND_TEST_SERVICE)
        else:
            logger.debug(f'ignore branch ==> {branch}')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    deploy_be('v0.0.5', 'refs/heads/dev')
