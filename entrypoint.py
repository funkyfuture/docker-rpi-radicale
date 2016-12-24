#!/usr/bin/env python

from configparser import ConfigParser
from os import environ, execlp
from pathlib import Path
from subprocess import check_call
from sys import stdout
from tempfile import gettempdir

from dulwich.errors import NotGitRepository
from dulwich.repo import Repo


COLLECTIONS_DIR = Path('/collections')
CONFIG_DIR = Path('/config')
CONFIG_PATH = CONFIG_DIR / 'radicale.ini'
INTERPOLATED_CONFIG_PATH = Path(gettempdir()) / 'radicale.ini'
RADICALE_USER = 'radicale'

DEFAULTS = {'auth': {'type': 'htpasswd',
                     'htpasswd_encryption': 'bcrypt',
                     'htpasswd_filename': str(CONFIG_DIR / 'users')},
            'logging': {'config': str(CONFIG_DIR / 'logging')},
            'rights': {'type': 'from_file',
                       'file': str(CONFIG_DIR / 'rights')},
            'storage': {'type': 'filesystem',
                        'filesystem_folder': str(COLLECTIONS_DIR)}}


def set_config(section, parameter, value):
    if not config.has_section(section):
        config[section] = {}
    config[section][parameter] = value


config = ConfigParser()

# read config file if present
if CONFIG_PATH.is_file():
    config.read(str(CONFIG_PATH))

# add / override config from environment variables
env_config = [(k[2:], v) for k, v in environ.items() if k.startswith('R_')]
if env_config:
    for key, value in env_config:
        section, parameter = key.lower().split('_', 1)
        if section == 'wellknown':
            section = 'well-known'
        set_config(section, parameter, value)

# set default config for missing parameters
for section, parameter_value in DEFAULTS.items():
    for parameter, value in parameter_value.items():
        if not config.has_section(section) or \
                parameter not in config[section]:
            set_config(section, parameter, value)

# write and print interpolated config
with INTERPOLATED_CONFIG_PATH.open('tw') as fd:
    config.write(fd)
with INTERPOLATED_CONFIG_PATH.open('tr') as fd:
    print('Interpolated configuration (%s):' % str(INTERPOLATED_CONFIG_PATH))
    print('=====')
    lines = fd.readlines()
    while not lines[-1].strip():
        lines.pop()
    print(''.join(lines))
    print('=====')

# initalize git-repo if necessary
if config['storage']['type'] == 'filesystem':
    collections_folder = config['storage']['filesystem_folder']
    try:
        Repo(collections_folder)
    except NotGitRepository:
        Repo.init(collections_folder)

# ensure ownership of RADICALE_USER
for path in (COLLECTIONS_DIR, CONFIG_DIR, INTERPOLATED_CONFIG_PATH):
    if path.is_dir():
        check_call(['chown', '-R', RADICALE_USER, str(path)])
    else:
        check_call(['chown', RADICALE_USER, str(path)])

# fork radicale as RADICALE_USER
stdout.flush()
execlp('su-exec', 'radicale', RADICALE_USER, 'radicale', '--config',
       str(INTERPOLATED_CONFIG_PATH))
