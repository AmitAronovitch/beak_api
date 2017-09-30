try:
    from inspect import signature
except ImportError:
    from funcsigs import signature
from bottle import route, default_app
from .. import config
from . import pyconil2016, pyconil2016_old, pyconil

app = application = default_app()

_api_names = []

def nadic_func_names(module, n):
    return [name for name in module.__all__
            if len(signature(getattr(module,name)).parameters)==n]

for apilib in [pyconil2016, pyconil2016_old, pyconil]:
    apiname = apilib.__name__.split(".")[-1]
    _api_names.append(apiname)
    suffix = getattr(apilib, 'cmd_suffix', '')

    @route('/api/{0}/list'.format(apiname))
    def list(apilib=apilib, suffix=suffix):
        return {'commands': [x+suffix for x in apilib.__all__]}

    cmd0_re = '|'.join(nadic_func_names(apilib, 0))
    cmd1_re = '|'.join(nadic_func_names(apilib, 1))
    cmd2_re = '|'.join(nadic_func_names(apilib, 2))
    
    if len(cmd0_re):
        @route('/api/{0}/<cmd:re:{1}>{2}'.format(apiname, cmd0_re, suffix))
        def api_call(cmd, apilib=apilib):
            return getattr(apilib, cmd)()
    
    if len(cmd1_re):
        @route('/api/{0}/<cmd:re:{1}>{2}/<p1>'.format(apiname, cmd1_re, suffix))
        def api_call(cmd, p1, apilib=apilib):
            return getattr(apilib, cmd)(p1)
    
    if len(cmd2_re):
        @route('/api/{0}/<cmd:re:{1}>{2}/<p1>/<p2>'.format(apiname, cmd2_re, suffix))
        def api_call(cmd, p1, p2, apilib=apilib):
            return getattr(apilib, cmd)(p1,p2)
    
@route('/api/list')
def list_apis():
    return {'apis': _api_names}

