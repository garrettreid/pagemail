from flask import session, request
from .database import get_db
from functools import wraps
from uuid import uuid4
from .util import gen_uuid

def track_user(email_id):
	c = get_db()
	c.execute("INSERT INTO views VALUES (?, strftime('%s', 'now'), ?, ?, ?)", (email_id, request.remote_addr, request.headers.get('User-Agent'), session['id']))
	get_db().commit()

## Decorators
def set_cookie(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		if not 'id' in session.keys():
			session['id'] = gen_uuid()
		return(f(*args, **kwargs))
	return decorator

