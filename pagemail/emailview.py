from database import get_db
from datetime import datetime
from flask import _app_ctx_stack
from pybrowscap.loader.csv import load_file
from sys import stdout
from os import path

class EmailView (object):
	def __init__(self, view_uuid=None, admin_uuid=None):
		c = get_db().cursor()

		# Look up the email by the appropriate identifier
		if view_uuid:
			c.execute("SELECT * FROM emails WHERE view_uuid=?", [view_uuid])
		elif admin_uuid:
			c.execute("SELECT * FROM emails WHERE admin_uuid=?", [admin_uuid])
		else:
			raise ValueError("Must specify either view or admin UUID")

		row = c.fetchone()
		if not row:
			raise LookupError("No such email")

		self.dbid = row[0]
		self.view_uuid = row[1] # matches view_uuid
		self.admin_uuid = row[2]
		self.sentfrom = row[3]
		self.subject = row[4]
		self.content = row[5]
		self._views = None

	@property
	def views(self):
		if not self._views:
			# First, fetch all views
			c = get_db().cursor()
			c.execute("SELECT * FROM views WHERE email=?", [self.dbid])
			views = c.fetchall()
			self._set_views(views)

			# Then, reformat the unix timestamp into a date
			#self._views = map(lambda r: [r[0], datetime.fromtimestamp(int(r[1])).strftime('%Y-%m-%d %H:%M:%S'), r[2], r[3], r[4]], self._views)

		return self._views

	def _set_views(self, views):
		self._views = []
		for line in views:
			date = datetime.fromtimestamp(int(line[1]))
			b = _get_browscap().search(line[3])
			browser = "%s / %s / %s / %s %s" % (b.device_maker(), b.device_name(), b.platform(), b.category(), b.version())
			self._views.append([line[0], date, line[2], browser, line[4]])

# Lazy loading wrapper for browscap
def _get_browscap():
	browscap = getattr(_app_ctx_stack, "_browscap", None)
	if browscap is None:
		print "Loading browscap... ",
		stdout.flush()
		browscap_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'browscap.csv')
		browscap =  _app_ctx_stack._browscap = load_file(browscap_path)
		print "done!"
	return browscap
