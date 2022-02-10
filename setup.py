#!/usr/bin/env python3

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='telemetrix-esp32',
    packages=['telemetrix_aio_esp32', 'telemetrix_esp32_common', 'telemetrix_esp32'],
    install_requires=['bleak'],

    version='1.1',

    description="Remotely Control And Monitor ESP32 Devices",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Alan Yorinks',
    author_email='MisterYsLab@gmail.com',
    url='https://github.com/MrYsLab/telemetrix-esp32',
    download_url='https://github.com/MrYsLab/telemetrix-esp32',
    keywords=['telemetrix', 'ESP32', 'Protocol', 'Python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
