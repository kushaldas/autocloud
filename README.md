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
