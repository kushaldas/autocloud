# Autocloud

## Setup

```
pip install -r requirements.txt
python setup.py develop
sudo mkdir -p /etc/autocloud; sudo cp config/autocloud.cfg /etc/autocloud/autocloud.cfg
python seed.py
```

## Run dashboard

```
python autocloud/web/app.py
```

## fedmsg config

Add the dictionary to endpoints in /etc/fedmsg.d/endpoints.py

```
"__main__.fedora-build": [
     "tcp://127.0.0.1:4321",
],
"autocloud.fedora-build": [
     "tcp://127.0.0.1:4322",
]
```

Change the topic in the fedmsg consumer hub to

```
topic = 'org.fedoraproject.dev.__main__.buildsys.task.state.change'
```
