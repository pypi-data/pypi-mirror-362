# setup.py

from setuptools import setup, find_packages

setup(
    name='django_maker',
    version='2.0.0',
    packages=find_packages(),
    package_data={
        'django_maker': ['management/commands/*'],
    },
    install_requires=[
        'Django>=3.0',
    ],
    description='A Python package for managing framework django',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
