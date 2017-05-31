from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='rapnet',
    version='2.1.5',
    description='An API Client Library for Rapnet for Python 3',
    long_description=long_description,
    url='https://github.com/codesigntheory/rapnet',
    author='Utsob Roy',
    author_email='utsob@codesign.com.bd',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords='rapnet API',
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    py_modules=["rapnet"],
    install_requires=['requests'],
)
