#!/usr/bin/python3
ingest_server = 'https://s.en0.io'
print('set ingest server to ' + ingest_server)
infile = open('/home/nlsd/key', 'r')
authkey = infile.readline()
import sys
from os.path import exists
import base64
import requests
import threading
from sh import tail


def trackufw():
    while True:
        for line in tail("-F", "/var/log/ufw.log", _iter=True):
            log_line_encoded = base64.b64encode(line.encode("utf-8"))
            payload = {'key': authkey, 'log': log_line_encoded}
            r = requests.post(ingest_server + '/api/v1/logevent/ufw', data=payload)
            print("ufw: " + r.text)


def tracksshd():
    while True:
        for line in tail("-F", "/var/log/fail2ban.log", _iter=True):
            log_line_encoded = base64.b64encode(line.encode("utf-8"))
            payload = {'key': authkey, 'log': log_line_encoded}
            r = requests.post(ingest_server + '/api/v2/logevent/sshd', data=payload)
            print("sshd: " + r.text)


threading.Thread(target=trackufw).start()

if (exists("/var/log/fail2ban.log")):
    threading.Thread(target=tracksshd).start()
