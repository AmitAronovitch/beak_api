try:
    from inspect import signature
except ImportError:
    from funcsigs import signature
import logging
import os
import os.path as op
import warnings
from importlib import import_module

from ..config import options

# hack: patch old versions of os.makedirs (TODO: does 'future' support this?)
if 'exist_ok' not in signature(os.makedirs).parameters:
    def makedirs(path, mode=0o777, exist_ok=False):
        if not op.exists(path):
            os.makedirs(path, mode)
else:
    makedirs = os.makedirs


def init_model(model, filename, initialize=False, debug=False):
    logging.debug('initializing {model} model, filename={0}, init={1}, debug={2}'.format(
        filename, initialize, debug, model=model.__name__))
    if debug:
        model.sql_debug(True)
    model.db.bind(provider='sqlite', filename=filename, create_db=initialize)
    model.db.generate_mapping(create_tables=initialize)


def _initialized(model):
    return model.db.provider is not None


def _load_data(model):
    try:
        load = import_module('.dataloader', model.__name__).load
    except ImportError:
        load = lambda: None
    return load()


def load(modelname):
    model = import_module('.' + modelname, __name__)
    if not _initialized(model):
        dbpath = op.abspath(getattr(options, modelname + '_db'))
        if op.isfile(dbpath):
            init_model(model, dbpath, debug=options.debug_sql)
        else:
            makedirs(op.dirname(dbpath), exist_ok=True)
            init_model(model, dbpath, initialize=True, debug=options.debug_sql)
            data = _load_data(model)
            if data:
                model.populate(data)
            else:
                warnings.warn('pyconil: Missing init data. DB will remain empty')
    return model
