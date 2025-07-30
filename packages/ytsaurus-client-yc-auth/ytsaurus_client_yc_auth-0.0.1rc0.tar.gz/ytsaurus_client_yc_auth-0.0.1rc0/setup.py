import os
from distutils.core import setup
from pathlib import Path
from setuptools import find_namespace_packages

setup(
    name='ytsaurus-client-yc-auth',
    version='0.0.1rc0',
    license='Apache-2.0',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: Apache Software License",
    ],
    author="Yandex LLC",
    author_email="cloud@support.yandex.ru",
    packages=find_namespace_packages(include=('yc_managed_ytsaurus_auth',)),
    install_requires=[
        'ytsaurus-client>=0.13.33,<0.14.0',
    ],
    python_requires=">=3.8",
    description='Yandex Cloud auth for YTsaurus client',
    long_description_content_type='text/markdown',
    long_description='Yandex Cloud auth for YTsaurus client',
)
