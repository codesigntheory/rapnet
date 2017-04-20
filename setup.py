from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rapnet',
    version='0.2.1',
    description='An API SDK for Rapnet for Python 3',
    long_description=long_description,
    url='https://github.com/uroybd/rapnet',
    author='Utsob Roy',
    author_email='uroybd@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='rapnet API',
    packages=find_packages(),
    install_requires=['requests'],
)