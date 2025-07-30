from os.path import join, dirname

from setuptools import setup

requirements = [
    'jsonpickle==0.7.1',
    'requests==2.26.0',
    'Jinja2==2.9.6',
    'MarkupSafe==2.0.1',
    'requests-unixsocket==0.1.5'
]

version = open(join(dirname(__file__), 'version')).read().strip()

setup(
    name='syncloud-lib',
    version=version,
    install_requires=requirements,
    description='Syncloud common library',
    packages=['syncloudlib', 'syncloudlib.integration', 'syncloudlib.application', 'syncloudlib.json'],
    license='GPLv3',
    author='Syncloud',
    author_email='syncloud@syncloud.it',
    url='https://github.com/syncloud/lib')

