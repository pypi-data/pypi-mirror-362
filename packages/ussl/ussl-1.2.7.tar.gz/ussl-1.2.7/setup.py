#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import platform

from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


if 'win' in sys.platform.lower():
    logging.info('For the LDAP protocol to work correctly, install the dependency:')
    if not platform.python_version().startswith('3.8'):
        logging.info('Find the version you need on https://github.com/cgohlke/python-ldap-build/releases/')
    if platform.architecture()[0] == '64bit':
        logging.info('\tpip install https://github.com/cgohlke/python-ldap-build/releases/download/v3.4.4/python_ldap-3.4.4-cp38-cp38-win_amd64.whl')
    elif platform.architecture()[0] == '32bit':
        logging.info('\tpip install https://github.com/cgohlke/python-ldap-build/releases/download/v3.4.4/python_ldap-3.4.4-cp38-cp38-win32.whl')
    else:
        logging.info('Find the version you need on https://github.com/cgohlke/python-ldap-build/releases/')


setup(
    name='ussl',
    author='ussc soc dev team',
    author_email='daniil.bessmertnykh@udv.group, miroslav.zenkov@udv.group',
    description='Пакет разработчиков USSC-SOC для упрощения взаимодействия с АРМ, серверами и сетевыми устройствами',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='1.2.7',
    python_requires='>=3.8.0',
    packages=[
        'ussl',
        'ussl.model',
        'ussl.postprocessing',
        'ussl.protocol',
        'ussl.exceptions',
        'ussl.utils',
    ],
    install_requires=[
        'pywinrm==0.4.3',
        'paramiko==3.3.1',
        'marshmallow==3.20.2',
        'python-ldap==3.4.4; platform_system != "Windows"',
        # 'python-ldap-build @ https://github.com/cgohlke/python-ldap-build/releases/download/v3.4.4/python_ldap-3.4
        # .4-cp38-cp38-win_amd64.whl', # for Windows only
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8'
    ]
)

# To update version:
# python setup.py sdist
# twine upload dist/*
