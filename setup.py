from setuptools import setup, find_packages

setup(
    name='pymaps',
    version='0.1',
    description='Sorted maps for python',
    author='Samuel Yvon',
    author_email='samuel.yvon@umontreal.ca',
    url='https://github.com/SamuelYvon/PyMaps',
    packages=find_packages(exclude=['contrib', 'docs', 'tests'])
)
