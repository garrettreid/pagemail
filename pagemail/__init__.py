"""
pagemail
--------

A collection of libraries for receiving emails,
rendering them as web pages, and tracking views
"""

__version__ = '1.0.0'
#from .database import get_db, close_db
from .database import close_db
from .emailview import EmailView
from .config import Config
from .track import set_cookie, track_user
from .util import gen_uuid, insert_email
