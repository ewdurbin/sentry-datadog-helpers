#!/usr/bin/env python
"""
sentry-datadog-helpers
======================
An suite of Sentry tools which enhance integrations with Datadog
"""
from setuptools import setup
from setuptools import find_packages

install_requires = []

raven_requires = [
    'raven>=5.6.0',
]

sentry_requires = [
    'sentry>=7.4.0',
    'datadog==0.9.0',
]

tests_require = [
    'mock==1.3.0',
] + raven_requires + sentry_requires

setup(
    name='sentry-datadog-helpers',
    version='1.4.0',
    author='Ernest W. Durbin III',
    author_email='ewdurbin@gmail.com',
    url='http://github.com/ewdurbin/sentry-datadog-helpers',
    description='Suite of Sentry tools which enhance integrations with Datadog.',
    long_description=__doc__,
    packages=find_packages(),
    extras_require={
        'raven': raven_requires,
        'sentry': sentry_requires,
        'tests': tests_require,
    },
    license='BSD',
    zip_safe=False,
    install_requires=install_requires,
    test_suite='tests',
    include_package_data=True,
    download_url='https://pypi.python.org/pypi/sentry-datadog-helpers',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
