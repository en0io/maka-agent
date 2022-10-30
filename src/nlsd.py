#!/usr/bin/python3
import os

ingest_server = "https://s.en0.io"

import base64
import threading
from os.path import exists

import requests
from sh import tail

authkey = os.environ.get("AUTHKEY")
if not authkey:
    infile = open("/home/nlsd/key", "r")
    authkey = infile.readline()


def trackufw():
    while True:
        for line in tail("-F", "/var/log/ufw.log", _iter=True):
            log_line_encoded = base64.b64encode(line.encode("utf-8"))
            payload = {
                "key": authkey,
                "log": log_line_encoded,
            }
            r = requests.post(
                ingest_server + "/api/v1/logevent/ufw",
                data=payload,
            )
            print("ufw: " + r.text)


def tracksshd():
    while True:
        for line in tail("-F", "/var/log/fail2ban.log", _iter=True):
            log_line_encoded = base64.b64encode(line.encode("utf-8"))
            payload = {
                "key": authkey,
                "log": log_line_encoded,
            }
            r = requests.post(
                ingest_server + "/api/v2/logevent/sshd",
                data=payload,
            )
            print("sshd: " + r.text)


def main():
    if exists("/var/log/ufw.log"):
        threading.Thread(target=trackufw).start()
    else:
        print("ufw log not found")

    if exists("/var/log/fail2ban.log"):
        threading.Thread(target=tracksshd).start()
    else:
        print("f2b log not found")


if __name__ == "__main__":
    main()
