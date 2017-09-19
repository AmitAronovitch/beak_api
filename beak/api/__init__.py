from bottle import route
from .. import config
config.init()
from . import pyconil2016_test, pyconil2016

_api_names = []

for apilib in [pyconil2016_test, pyconil2016]:
    apiname = apilib.__name__.split(".")[-1]
    _api_names.append(apiname)
    
    cmd_re = '|'.join(apilib.__all__)
    @route('/api/{0}/<cmd:re:{1}>'.format(apiname, cmd_re))
    def api_call(cmd, apilib=apilib):
        return getattr(apilib, cmd)()

    @route('/api/{0}/list'.format(apiname))
    def list(apilib=apilib):
        return {'commands': apilib.__all__}

@route('/api/list')
def list_apis():
    return {'apis': _api_names}

