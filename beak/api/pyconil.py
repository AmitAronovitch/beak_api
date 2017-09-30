from ..utils import public
from ..model import load as model_load

model = model_load('pyconil')

@public
@model.db_session
def speakers():
    return {
        'speakers': [x.to_dict() for x in model.Speaker.select()]
    }

def session2dict(s):
    d = s.to_dict()
    d['time'] = d['time'].strftime('%Y-%m-%d %H:%M')
    d['duration'] = str(d['duration'])
    return d

@public
@model.db_session
def sessions():
    return {
        'sessions': [session2dict(x) for x in model.Session.select()]
    }

@public
@model.db_session
def speaker_sessions(sid):
    #todo: fail if not int
    sessions = model.Speaker[int(sid)].sessions
    return {'sessions': [session2dict(x) for x in sessions]}

