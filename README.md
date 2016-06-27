# Autocloud

## Setup

```
sudo dnf install fedfind

pip install -r requirements.txt
python setup.py develop
sudo mkdir -p /etc/autocloud; sudo cp config/autocloud.cfg /etc/autocloud/autocloud.cfg
```

## Development

### Create the database

```
python createdb.py
```

### Run the fedmsg-hub

```
fedmsg-hub
```

### Publish messages for testing

Run this command in a seperate terminal

```
python publish/publish_messages.py
```

### Applying the migrations

```
alembic upgrade head
```
