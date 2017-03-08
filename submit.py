#!/usr/bin/env python
import sys
import email
import smtplib
from os import path
from email.mime.text import MIMEText
sys.path.append(path.dirname(path.abspath(__file__)))
from pagemail import insert_email, Config

# Settings
config = Config()
full_address = "%s <%s>" % (config['email']['name'], config['email']['address'])

# Read in the email, pull out necessary bits
message = email.message_from_file(sys.stdin)
sender = message['from']
sender_name, sender_address = email.utils.parseaddr(sender)
subject = message['subject']
reply_to = message['message-id']
delivered_to = message['delivered-to']
to_name, to_address = email.utils.parseaddr(delivered_to)

# Some quick defensive hacks to minimize abuse
# As per /usr/include/sysexits.h
# #define EX_NOUSER       67      /* addressee unknown */
if to_address != config['email']['address']:
	sys.exit(67)
if sender_address not in config['email']['senders']:
	sys.exit(67)

# If we're multipart, grab part prioritized in config
content = None
if message.is_multipart():
	best_index = -1
	for part in message.walk():
		content_type = part.get_content_type()
		try:
			index = config['email']['types'].index(content_type)
		except ValueError:
			index = -1

		if index > best_index:
			best_index = index
			content = part.get_payload(decode=True)
else:
	content = message.get_payload(decode=True)

# If we extracted valid content, take action and send a nice reply
if content is not None:
	record_sender = sender
	if config['email']['replacements']:
		# use sender_name, sender_address from above
		sender_index = config['email']['senders'].index(sender_address)
		new_address = config['email']['replacements'][sender_index]
		record_sender = "%s <%s>" % (sender_name, new_address)

	view_uuid,admin_uuid = insert_email(record_sender, subject, content)
	view_url = "https://%s/view/%s/" % (config['web']['domain'], view_uuid)
	admin_url = "https://%s/admin/%s/" % (config['web']['domain'], admin_uuid)
	msg = MIMEText(config.format_success(subject, view_url, admin_url), "plain", "utf-8")
else:
	msg = MIMEText(config['email']['failure'], "plain", "utf-8")

# Now that we have message content, set the remaining headers
msg['From'] = full_address
msg['To'] = sender
msg['Subject'] = "Re: %s" % subject
msg['In-Reply-To'] = reply_to
msg['References'] = reply_to

# And fire off our reply
smtp = smtplib.SMTP('localhost')
smtp.sendmail(full_address, [sender], msg.as_string())
smtp.quit()

sys.exit(0)
