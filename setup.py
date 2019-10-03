from setuptools import setup, find_packages

requires = [
    'requests',
    'tzlocal',
    'lxml',
    'pytz',
    'pymongo',
    'PyYAML'
]

dev_requires = [
    'pipreqs'
]

setup(
    name='mlb-stats',
    version='0.0.1',
    author='Riley Raschke',
    author_email='riley@rrappsdev.com',
    packages=['mlbstats.service'],
    scripts=['get-stats-terminal.py'],
    url='ssh://scm.rrappsdev.com/var/git/mlb-stats.git', # this should be github....
    license='LICENSE',
    description='Cache-ify MLB stats from ESPN.com',
    long_description='Pull MLB stats from ESPN and cache them to mongo database',
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    }
)

