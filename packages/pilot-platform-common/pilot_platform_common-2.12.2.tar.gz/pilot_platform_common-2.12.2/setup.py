# Copyright (C) 2022-2025 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()

setuptools.setup(
    name='pilot-platform-common',
    version='2.12.2',
    author='Indoc Systems',
    author_email='support@indocsystems.com',
    description='Generates entity ID and connects with Vault (secret engine) to retrieve credentials',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10,<3.13',
    install_requires=[
        'python-dotenv>=0.19.1',
        'httpx==0.28.1',
        'redis>=4.5.0,<7.0.0',
        'aioboto3==14.3.0',
        'xmltodict==0.14.2',
        'minio==7.2.15',
        'python-json-logger==2.0.2',
        'pyjwt==2.10.1',
        'starlette>=0.40.0,<0.47.0',
        'requests>=2.26.0,<2.32.0',
        'cryptography==44.0.2',
        'pydantic>=2.7.1,<3.0.0',
    ],
    include_package_data=True,
    package_data={
        '': ['*.crt'],
    },
)
