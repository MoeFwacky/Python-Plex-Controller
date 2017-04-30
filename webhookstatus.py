import os
import subprocess
import time

command = "ps aux | grep tbn_webhook_service.py | grep -v grep"
try:
	stuff = subprocess.check_output(command, shell=True)
except subprocess.CalledProcessError:
	stuff = ""

if "tbn_webhook_service.py" in stuff:
	print ("The Webhook Service script is running")
else:
	print ("The Webhook Service script is not running. Trying to restart.")
	command = "python " + homedir + "tbn_webhook_service.py >/dev/null &"
	os.system(command)
	time.sleep(1)
	command = "ps aux | grep tbn_webhook_service.py | grep -v grep"
	stuff = subprocess.check_output(command, shell=True)
	if "tbn_webhook_service.py" in stuff:
		print ("The Webhook Service script is running")
	else:
		print ("Error: Failed to automatically start tbn_webhook_service.py.")

