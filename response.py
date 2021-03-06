#!/usr/bin/env python2
# -*- coding=UTF-8 -*-
# Created at Jul 16 15:59 by BlahGeek@Gmail.com

import sys
import os
import logging
from msg import NO_HANDLER, HANDLE_ERROR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weixin.settings")

from plugins import Plugin
from plugins import *

def response(text, userid):
    plugins = map(lambda x: x(), iter(Plugin))
    try:
        plugin = max(plugins, key=lambda x: x.predict(text))
    except ValueError:
        logging.warn('No handler available.')
        return NO_HANDLER
    logging.info('Using handler: %s' % str(plugin))
    try:
        ret = plugin.handle(text, userid)
    except RuntimeError:
        ret = HANDLE_ERROR
    return ret

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import django
    django.setup() 
    print response(sys.argv[1].decode('utf8'), 
        'default' if len(sys.argv) < 3 else sys.argv[2])
