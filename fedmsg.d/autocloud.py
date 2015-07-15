import socket
hostname = socket.gethostname().split('.')[0]


config = {
    # Consumer stuff
    "autocloud.consumer.enabled": True,
    "autocloud.sqlalchemy.uri": "sqlite:////var/tmp/autocloud-dev-db.sqlite",

    # Turn on logging for autocloud
    "logging": dict(
        loggers=dict(
            autocloud={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
}
