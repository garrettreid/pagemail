#!/usr/bin/python
activate_this = '/var/www/pagemail/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pagemail/")

from run import app as application
from pagemail import Config
config = Config()
application.secret_key = config['web']['secret']
