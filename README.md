# Autocloud

## Setup

```
pip install -r requirements.txt
python setup.py develop
sudo mkdir /etc/autocloud; sudo cp config/autocloud/cfg /etc/autocloud/autocloud.cfg
python seed.py
```

## Run dashboard

```
python autocloud/web/app.py
```

## Test local fedmsg

Add the dictionary to endpoints in /etc/fedmsg.d/endpoints.py

```
"__main__.localhost": [
    "tcp://127.0.0.1:4321",
]
```
