from uuid import uuid4
from .database import _open_database_connection

# Generates a nicely-formatted non-identifying UUID
def gen_uuid():
	# It's easier to split URN than insert -s into hex
	return uuid4().urn.split(':')[-1].upper()

# Inserts an email, returns (view_uuid, admin_uuid)
def insert_email(sender, subject, content):
	db = _open_database_connection()
	c = db.cursor()

	view_uuid = gen_uuid()
	admin_uuid = gen_uuid()
	c.execute("INSERT INTO emails (view_uuid, admin_uuid, sentfrom, subject, content) VALUES (?, ?, ?, ?, ?)", [view_uuid, admin_uuid, sender, subject, content.decode('utf-8')])
	db.commit()
	return (view_uuid, admin_uuid)
