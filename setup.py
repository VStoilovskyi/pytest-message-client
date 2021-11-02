"""Config for setup package pytest agent."""

import os

from setuptools import setup


__version__ = '1.0.0b'


def read_file(fname):
    """Read the given file."""
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='pytest-message',
    version=__version__,
    description='Pytest plugin for sending report message of marked tests execution',
    author_email='vadym.stoilovskyi@gmail.com',
    url='https://github.com/VStoilovskyi/pytest-message',
    packages=['pytest'],
    install_requires=read_file('requirements.txt').splitlines(),
    license='Apache 2.0',
    keywords=['notify', 'pytest', 'message'],
    classifiers=[
        'Framework :: Pytest',
        'Programming Language :: Python :: 3.8'
        ],
    entry_points={
        'pytest11': [
            'pytest_message = pytest_message.plugin',
        ]
    }
)