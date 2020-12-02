#!/usr/bin/env python
from os import path
from configparser import ConfigParser
from string import Template

# This would be better as a singleton
class Config (object):
	def __init__(self):
		conf_path = path.join(path.dirname(__file__), '..', 'pagemail.conf')
		self.conf = ConfigParser()
		self.conf.read(conf_path)
		e = {}
		w = {}

		# Macro to shorten email fetch lines
		ge = lambda k, d: self._getconf('email', k, d)
		e['name'] = ge('email_name', 'PageMail')
		e['address'] = ge('email_address', 'pagemail@yourdomain.tld')
		e['success'] = ge('success_text', 'Subject: $subject, view: $view_url, admin: $admin_url')
		e['failure'] = ge('failure_text', "Couldn't find a good MIME part")

		# Unpack our lists
		e['senders'] = ge('senders_list', None)
		if e['senders']:
			e['senders'] = e['senders'].split(",")
		e['replacements'] = ge('sender_replacements', None)
		if e['replacements']:
			e['replacements'] = e['replacements'].split(",")
		e['types'] = ge('mime_types', 'text/plain,text/html').split(",")

		# Macro to shorten web fetch lines
		gw = lambda k, d: self._getconf('web', k, d)
		w['name'] = gw('sitename', 'PageMail')
		w['domain'] = gw('domain', 'yourdomain.tld')
		w['name'] = self._getconf('web', 'sitename', 'PageMail')
		# If the secret isn't set, things should fail to run
		w['secret'] = self.conf.get('web', 'cookie_secret')

		self._email = e
		self._web = w

	# An ugly hack, but keeps formatting logic internal to config
	def format_success(self, subject, view_url, admin_url):
		template = Template(self._email['success'])
		templatemap = {'subject': subject, 'view_url': view_url, 'admin_url': admin_url}
		return template.substitute(templatemap)

	# Provide a nested "dictionary" interface
	def __getitem__(self, key):
		if key == "email":
			return self._email
		if key == "web":
			return self._web

		# We don't have any other keys
		return None

	def _getconf(self, section, key, default):
		value = default
		try:
			value = self.conf.get(section, key)
		except:
			# Key undefined in this section
			pass

		return value
