# maka-agent

python service for the project maka service (https://s.en0.io)

To get the API key for this, visit https://s.en0.io/account/edit

## Installation: Docker
```
docker build -t nlsd --force-rm .
docker run -d --restart=always --name nlsd -e AUTHKEY=AUTHKEY -v /var/log:/var/log:ro nlsd
```

## Installation: Host
```
apikey=YOUR_API_KEY_GOES_HERE
hostname=`hostname`
useradd nlsd
chsh nlsd -s /bin/bash
mkdir /home/nlsd/
cp /etc/skel/.bashrc /etc/skel/.profile /home/nlsd/
curl -s -X POST https://s.en0.io/api/createReporter -H "Content-Type: application/x-www-form-urlencoded" -d "key=$apikey&hostname=$hostname" | python3 -c "import sys, json; print(json.load(sys.stdin)['message'])" > /home/nlsd/key
wget https://raw.githubusercontent.com/en0io/maka-agent/main/src/nlsd.py -O /home/nlsd/nlsd.py
chmod +x nlsd.py
chown -R nlsd:nlsd /home/nlsd
chmod -R 770 /home/nlsd
adduser nlsd adm
runuser -l nlsd -c 'pip3 install sh requests'
wget https://raw.githubusercontent.com/en0io/maka-agent/main/src/nlsd.service -O /etc/systemd/system/nlsd.service
systemctl enable nlsd.service
systemctl start nlsd.service
chsh nlsd -s /usr/sbin/nologin
```
