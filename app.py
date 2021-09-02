from flask import Flask
from flask import request
import json
from . import deploy_fe
from logger import logger

# 部署地址
WEB_DEV_SERVICE = 'web-dev'
WEB_TEST_SERVICE = 'web-test'
BACKEND_TEST_SERVICE = 'backend-test'
BACKEND_DEV_SERVICE = 'backend-dev'


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.form.get('payload')
    if payload:
        payload = json.loads(payload)
        ref = payload.get('ref')
        base_ref = payload.get('base_ref')
        logger.debug(ref, base_ref)
        if ref.startswith('refs/tags'):
            tag = ref.split("/")[-1]
            if base_ref == 'refs/heads/dev':
                logger.debug('start deploy dev')
                deploy_fe(tag, WEB_DEV_SERVICE)
            else:
                logger.debug('start deploy test')
                deploy_fe(tag, WEB_TEST_SERVICE)
        else:
            logger.debug('ignore commit')
    else:
        logger.debug(payload)
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
