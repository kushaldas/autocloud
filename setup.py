from setuptools import setup

requires = [
    'SQLAlchemy>=0.8',
    'redis',
    'retask',
    'fedmsg',
    'jenkinsapi',
    'flask'
]

setup(
    name='autocloud',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='https://github.com/kushaldas/autocloud',
    install_requires=requires,
    packages=['autocloud'],
    entry_points={
        'moksha.consumer': [
            "autocloud_consumer = autocloud.consumer:AutoCloudConsumer",
        ],
    },
)
