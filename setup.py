from setuptools import setup

requires = [
    'fedmsg',
]

setup(
    name='autocloud',
    version='0.0.1',
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

