#!/usr/bin/python3
ingest_server = 'https://s.en0.io'
ingest_endpoint = '/api/v1/logevent/ufw'
print('set ingest server to ' + ingest_server)
infile = open('/home/nlsd/key', 'r')
authkey = infile.readline()
import sys
import base64
import requests
from sh import tail
for line in tail("-F", "/var/log/ufw.log", _iter=True):
    log_line_encoded = base64.b64encode(line.encode("utf-8"))
    payload = {'key': authkey, 'log': log_line_encoded}
    r = requests.post(ingest_server + ingest_endpoint, data=payload)
    print(r.text)
