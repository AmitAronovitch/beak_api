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
    debug_sql = True, #False, # deduce from log_level?
    log_level = logging.DEBUG, #logging.INFO
    pyconil2016_db = op.join(ad.user_data_dir(appname, appauthor),
                           'pyconil2016.sqlite')
)

def read_config(path, keys):
    d = {}
    exec(open(path).read(), d)
    return dict( (k, d[k]) for k in d if k in keys )

def read_options_file(options, fname):
    for confdir in [ad.site_config_dir(appname, appauthor),
                    ad.user_config_dir(appname, appauthor)]:
        path = op.join(confdir, fname)
        print('----->checking {0}'.format(path))
        if op.isfile(path):
            print('----->reading config from {0}'.format(path))
            options._config_path = path
            options.__dict__.update(read_config(path, options._keys))

def init():
    read_options_file(options, 'options.py')
    logging.basicConfig(level=options.log_level)
    logging.debug('options = {0}'.format(options.__dict__))
    data_dir = ad.user_data_dir(appname, appauthor)
    if (options._config_path is None) and not op.isdir(data_dir):
        os.makedirs(data_dir)

        
