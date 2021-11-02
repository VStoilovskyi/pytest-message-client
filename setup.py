"""Config for setup package pytest agent."""
from setuptools import setup

__version__ = '0.1.0b0'

setup(
    name='pytest-message',
    version=__version__,
    description='Pytest plugin for sending report message of marked tests execution',
    author_email='vadym.stoilovskyi@gmail.com',
    url='https://github.com/VStoilovskyi/pytest-message',
    packages=['pytest_message'],
    install_requires=['pytest>=6.2.5', 'slack-sdk==3.11.2'],
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
