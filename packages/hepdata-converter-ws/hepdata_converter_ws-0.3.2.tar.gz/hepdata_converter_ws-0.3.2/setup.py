# -*- coding: utf-8 -*-
from setuptools import setup
import re

test_requirements = [
    'coverage',
]

extras_require = {
    'tests': test_requirements,
}

def get_version():
    with open('hepdata_converter_ws/version.py', 'r') as version_f:
        content = version_f.read()

    r = re.search('^__version__ *= *\'(?P<version>.+)\'', content, flags=re.MULTILINE)
    if not r:
        return '0.0.0'
    return r.group('version')


# Get the long description from the README file
with open('README.md', 'rt') as fp:
    long_description = fp.read()


setup(
    name='hepdata-converter-ws',
    version=get_version(),
    install_requires=[
        'hepdata-converter>=0.3.3',
        'flask',
        'sentry-sdk[flask]',
    ],
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            'hepdata-converter-ws = hepdata_converter_ws:main',
        ]
    },
    packages=['hepdata_converter_ws'],
    url='https://github.com/HEPData/hepdata-converter-ws',
    license='GPL',
    author='HEPData Team',
    author_email='info@hepdata.net',
    description='Flask webservices enabling usage of hepdata-converter as a separate server over the network',
    download_url='https://github.com/HEPData/hepdata-converter-ws/tarball/%s' % get_version(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7'
)
