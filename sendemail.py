import pyzmail
import getpass
import sys
import time
import threading 

class Progressbar(threading.Thread):
	"""docstring for progress_bar_loading"""
	def __init__(self):
		threading.Thread.__init__(self)
		self.event = threading.Event()

	def run(self):
		print 'Sending....  ',
		sys.stdout.flush()

		event = self.event

		i = 0 
		while not event.is_set():
			if (i%4) == 0:
				sys.stdout.write('\b/')
			elif (i%4) == 1:
				sys.stdout.write('\b-')
			elif (i%4) == 2:
				sys.stdout.write('\b\\')
			elif (i%4) == 3:
				sys.stdout.write('\b|')

			sys.stdout.flush()
			event.wait(0.2)
			i+=1

		print '\b\b done!',

	def stop(self):
		self.event.set()

		
sending_from = raw_input('Sender: ')
sender=(sending_from.split('@')[0], sending_from)
recipients=tuple(str(x) for x in raw_input('Recipients: ').split(','))
subject= raw_input('Subject: ')
text_content= raw_input('Content: ')
prefered_encoding='iso-8859-1'
text_encoding='iso-8859-1'

payload, mail_from, rcpt_to, msg_id = pyzmail.compose_mail(\
	sender, \
	recipients, \
	subject, \
	prefered_encoding, \
	(text_content, text_encoding), \
	html=None)

print 'Sender: ', mail_from
print 'Recepient: ', rcpt_to
smtp_host = 'smtp.gmail.com'
smtp_port = 587
smtp_mode = 'tls'
smtp_login = raw_input('username: ')
smtp_pwd = getpass.getpass()

progress_bar = Progressbar()
progress_bar.start()

try:
	time.sleep(1)
	ret = pyzmail.send_mail(payload, mail_from, rcpt_to, smtp_host, \
					smtp_port=smtp_port, smtp_mode=smtp_mode, \
					smtp_login=smtp_login, smtp_password=smtp_pwd)
	progress_bar.stop()
	progress_bar.join()
except KeyboardInterrupt or EOFError, e:
	print '\n! Received keyboard interrupt, quitting the app.\n'
	exit()


if isinstance(ret, dict):
	if ret:
		print 'failed recipient:', ', '.join(ret.keys())
	else:
		print 'success!'
else:
	print 'error:', ret
