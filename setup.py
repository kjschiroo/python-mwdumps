from setuptools import setup

setup(
    name='mwdumps',
    version='0.1',
    description='Module for downloading Wikimedia dumps',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',

    packages=['mwdumps'],
    install_requires=['docopt', 'beautifulsoup4', 'python-dateutil', 'requests']
)
