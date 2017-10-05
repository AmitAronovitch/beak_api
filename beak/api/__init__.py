from bottle import route, default_app
from ..utils import positional_args
from ..config import options
from . import pyconil2016, pyconil2016_old, pyconil

app = application = default_app()
root = options.api_root
if root.endswith('/'): root = root[:-1]

_api_names = []

def nadic_func_names(module, n):
    return [name for name in module.__all__
            if len(positional_args(getattr(module,name)))==n]

def api_signature(module, funcname, suffix):
    params = positional_args(getattr(module, funcname))
    return '/'.join(
        [funcname+suffix] + ['<{}>'.format(x) for x in params])

for apilib in [pyconil2016, pyconil2016_old, pyconil]:
    apiname = apilib.__name__.split(".")[-1]
    _api_names.append(apiname)
    suffix = getattr(apilib, 'cmd_suffix', '')

    @route(root+'/{0}/list'.format(apiname))
    def list(apilib=apilib, suffix=suffix):
        commands = [api_signature(apilib, x, suffix)
                    for x in apilib.__all__]
        return {'commands': commands}
    
    cmd0_re = '|'.join(nadic_func_names(apilib, 0))
    cmd1_re = '|'.join(nadic_func_names(apilib, 1))
    cmd2_re = '|'.join(nadic_func_names(apilib, 2))
    
    if len(cmd0_re):
        @route(root+'/{0}/<cmd:re:{1}>{2}'.format(apiname, cmd0_re, suffix))
        def api_call(cmd, apilib=apilib):
            return getattr(apilib, cmd)()
    
    if len(cmd1_re):
        @route(root+'/{0}/<cmd:re:{1}>{2}/<p1:int>'.format(apiname, cmd1_re, suffix))
        def api_call(cmd, p1, apilib=apilib):
            return getattr(apilib, cmd)(p1)
    
    if len(cmd2_re):
        @route(root+'/{0}/<cmd:re:{1}>{2}/<p1:int>/<p2:int>'.format(apiname, cmd2_re, suffix))
        def api_call(cmd, p1, p2, apilib=apilib):
            return getattr(apilib, cmd)(p1,p2)
    
@route(root+'/list')
def list_apis():
    return {'apis': _api_names}

