from setuptools import setup, find_packages

from os import path
from io import open

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-zoho-subscriptions',
    version='0.0.1',
    url='https://github.com/st8st8/django-zoho-subscriptions/',
    description='A simple python/django wrapper for the Zoho Subscriptions API compatible with Python 3.7',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Quintus Labs/PC Five',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ],
    keywords=('Django', 'Zoho', 'Subscriptions', 'Python 3',),
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests>=2.22.0',
        'gcloud>=0.18.3',
        'oauth2client>=4.1.3',
        'requests_toolbelt>0.9.1',
        'python_jwt>=3.2.4',
        'pycryptodome>=3.9.0',
        'urllib3>=1.25.5'
    ]
)
