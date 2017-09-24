import os, os.path as op
import logging
import appdirs as ad

appname = 'beakapi'
appauthor = 'Hamakor'

class Options(object):
    def __init__(self, *args, **keys):
        self.__dict__ = dict(*args, **keys)
        self._keys = set(x for x in self.__dict__ if not x.startswith('_'))

options = Options(
    _config_path = None,
    
    log_level = logging.INFO,
    debug_sql = False,
    pyconil2016_db = op.join(ad.user_data_dir(appname, appauthor),
                             'pyconil2016.sqlite'),
    # following are only used for the standalone runner (beak.api.run)
    host = '127.0.0.1',
    port = 8080,
)

options_glob = dict(
    [(x, getattr(logging,x)) for x in [
        'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'] ],
    environ = os.environ
)

def read_config(path, keys, globs={}):
    d = dict(**globs)
    exec(open(path).read(), d)
    return dict( (k, d[k]) for k in d if k in keys )

def read_options_file(options, fname):
    for confdir in [ad.site_config_dir(appname, appauthor),
                    ad.user_config_dir(appname, appauthor)]:
        path = op.join(confdir, fname)
        # Note: logging level here is BEFORE the config was read. Typically INFO
        logging.debug('checking for config at {0}'.format(path))
        if op.isfile(path):
            logging.debug('reading config from {0}'.format(path))
            options._config_path = path
            options.__dict__.update(read_config(
                path, options._keys, options_glob))

def init():
    read_options_file(options, 'options.py')
    logging.getLogger().setLevel(options.log_level)
    logging.debug('options = {0}'.format(options.__dict__))
    data_dir = ad.user_data_dir(appname, appauthor)
    if (options._config_path is None) and not op.isdir(data_dir):
        os.makedirs(data_dir)
