from distutils.core import setup

setup(
    name='journald-monitor',
    packages=['journald_monitor'],
    version='0.1',
    license='Apache License 2.0',
    description='Matches every line of journald with a list of regexes and executes action if a match is found',
    author='Gabriel Guldner',
    author_email='gabriel@guldner.eu',
    url='https://github.com/dasbaumwolltier/journald-monitor',
    download_url='https://github.com/dasbaumwolltier/journald-monitor/archive/v0.1.tar.gz',
    keywords = [
        'journald',
        'monitor',
        'journalctl'
    ],
    install_requires = [
        'pyyaml'
    ],
    extras_require = {
        'Matrix': ['matrix_client'],
        'Database': ['pyodbc'],
        'Telegram': ['requests']
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring'
    ],
    python_requires='>=3',
    entry_points = {
        'console_scripts': ['journald-monitor=journald_monitor.journald_monitor:main']
    }
)
