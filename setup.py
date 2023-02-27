from setuptools import find_packages
from setuptools import setup

packages = find_packages()
setup(
    name='flaskr',
    version='1.0.0',
    packages=packages,
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)