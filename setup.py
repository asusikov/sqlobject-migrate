import os
from setuptools import setup

# Utility function to read the README file.  
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sqlobjectmigrate",
    version = "0.0.21",
    author = "Alexander Susikov",
    author_email = "susikov.alexander@gmail.com",
    description = (""),
    license = "BSD",
    packages=['sqlobjectmigrate'],
    include_package_data=True,
    long_description=read('README'),
    install_requires = ['mako'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'console_scripts': ['sqlobject-migrate = sqlobjectmigrate.migrate:main'],
    },
)
