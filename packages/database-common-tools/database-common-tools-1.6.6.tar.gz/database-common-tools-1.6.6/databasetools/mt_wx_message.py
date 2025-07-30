# -*- coding: utf-8 -*-

import requests
import logging

##################################################
# post function
##################################################

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)
LOG_FT = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(LOG_FT)


def sendErrorMessage(receivers, subject, content, url):
    datas = dict()
    datas['receiver'] = receivers
    datas['subject'] = subject
    datas['content'] = str(content)
    try:
        requests.post(url=url, data=datas)
    except Exception as e:
        LOG.error('{} exception ... {}\tvalue={}'.format(subject, e, datas))
