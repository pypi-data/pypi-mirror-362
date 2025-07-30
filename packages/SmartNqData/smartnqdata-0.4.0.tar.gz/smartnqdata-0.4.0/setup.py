# setup.py

from setuptools import setup, find_packages

setup(
    name='SmartNqData',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'pytz',
        'pika'
    ],
    author='Alireza Keyanjam',
    author_email='akj@smartnq.com',
    description='An internal package to fetch market data from smartnq.com',
    long_description_content_type='text/markdown',
    url='https://github.com/alirezakeyanjam/araTrade.Database',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
