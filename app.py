from flask import Flask
from flask import request
import json
from deploy_fe import deploy_fe
from deploy_be import deploy_be
from logger import logger

# 部署地址
WEB_DEV_SERVICE = 'web-dev'
WEB_TEST_SERVICE = 'web-test'
BACKEND_TEST_SERVICE = 'backend-test'
BACKEND_DEV_SERVICE = 'backend-dev'
WEB_REPO_NAME = 'solhedge-fe'
BACKEND_REPO_NAME = 'solhedge-be'


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.get('payload')
    logger.debug(payload)
    if payload:
        payload = json.loads(payload)
        ref = payload.get('ref')
        base_ref = payload.get('base_ref')
        logger.debug(f'ref=>{ref}')
        logger.debug(f'base_ref=>{base_ref}')
        if ref.startswith('refs/tags'):
            repo_name = payload['repository']['name']
            logger.debug(f'repo_name=>{repo_name}')
            if repo_name == WEB_REPO_NAME:
                tag = ref.split("/")[-1]
                if base_ref == 'refs/heads/dev':
                    logger.debug('start deploy web dev')
                    deploy_fe(tag, WEB_DEV_SERVICE)
                elif base_ref == 'refs/heads/test':
                    logger.debug('start deploy web test')
                    deploy_fe(tag, WEB_TEST_SERVICE)
            elif repo_name == BACKEND_REPO_NAME:
                tag = ref.split("/")[-1]
                if base_ref == 'refs/heads/dev':
                    logger.debug('start deploy backend dev')
                    deploy_be(tag, BACKEND_DEV_SERVICE)
                elif base_ref == 'refs/heads/test':
                    logger.debug('start deploy backend test')
                    deploy_be(tag, BACKEND_TEST_SERVICE)
        else:
            logger.debug('ignore commit')
    else:
        logger.debug(payload)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
