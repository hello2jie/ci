from flask import Flask
from flask import request
import json
from deploy_fe import deploy_fe
from deploy_be import deploy_be
from logger import logger

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
            tag = ref.split("/")[-1]
            if repo_name == WEB_REPO_NAME:
                deploy_fe(tag, base_ref)
            elif repo_name == BACKEND_REPO_NAME:
                deploy_be(tag, base_ref)
        else:
            logger.debug('ignore commit')
    else:
        logger.debug(payload)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
