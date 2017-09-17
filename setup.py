from setuptools import setup

setup(
    name='mwdumps',
    version='0.2',
    description='Module for downloading Wikimedia dumps',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',

    packages=['mwdumps'],
    entry_points = {
        'console_scripts': ['mwdumps=mwdumps.cmdline:main'],
    },
    install_requires=[
        'docopt', 'beautifulsoup4', 'python-dateutil', 'requests'
    ]
)
