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
    packages=['autocloud', 'autocloud.web', 'autocloud.utils'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    entry_points={
        'moksha.consumer': [
            "autocloud_consumer = autocloud.consumer:AutoCloudConsumer",
        ],
    },
)
