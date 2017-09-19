import os.path as op
from ..config import options
from ..model import pyconil2016 as model

__all__ = []

def public(func):
    __all__.append(func.__name__)
    return func

#DATA_DIR = '../data/2016'

API_STATIC = () #'checkUpdates', 'getInfo', 'getSettings', 'getPOI'

API_TABLES = [
    ('getLevels','levels'),
    ('getLocations','locations'),
    ('getSpeakers','speakers'),
    ('getTypes','types'),
    ('getTracks','tracks'),
    ]

API_SESSION_TYPES = [
    ('getBofs', []),
    ('getSocialEvents', ['After party']),
    ]

# Notes re: Pony schemas
# * email contains nulls (not empty strings, nullable=True)
# * on firstName we need autostrip=False,

# static commands (use saved json)

#def checkUpdates():
#    return {'idsForUpdate': [0, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12]}

#for funcname in API_STATIC:
#    def _func(funcname=funcname):
#        return json.load(
#            open('{0}/{1}.json'.format(DATA_DIR, funcname)) )
#    _func.__name__ = _func.func_name = funcname
#    locals()[funcname] = model.db_session(_func)

#@model.db_session
#def getTypes():
#    return {'types': [x.to_dict() for x in model.Types.select()]}

# Level, Type, Location, Speaker
for funcname,tab in API_TABLES:
    dbname = tab[:-1].capitalize()
    def _func(tab=tab, dbname=dbname):
        return {tab: [x.to_dict() for x in getattr(model.dbname).select()]}
    _func.__name__ = _func.func_name = funcname
    locals()[funcname] = public(model.db_session(_func))

# Queries on the Event table
    
def emulate_old_format(data):
    "convert Event's json to old data format"
    # from and to had also "+0000", but that's just wrong
    data['from'] = data['from'] + '+0000'
    data['to'] = data['to'] + '+0000'
    # original API did not have the youtube link
    data['link'] = ''

#_old_event_format = False

def event2dict(e):
    d = e.to_dict()
    if d['experienceLevel'] is None:
        d['experienceLevel'] = 0
    d['from'] = d.pop('from_').isoformat()
    d['to'] = d['to'].isoformat()
    d['speakers'] = [x.speakerId for x in e.speakers]
    #if _old_event_format: emulate_old_format(d)
    return d

@public
@model.db_session
def getSessions(test=False):
    days = model.select(e.from_.date() for e in model.Event)[:]
    sessions = {
        'days': [
            {'date': d.strftime('%d-%m-%Y'),
             'events': map(event2dict,
                           model.Event.select(lambda e: e.from_.date()==d) )
            }
            for d in days]
        }
    return sessions

@model.db_session
def events_by_types(type_names):
    evtypes = model.Type.select(lambda t: t.typeName in type_names)
    days = model.select(e.from_.date() for e in model.Event
                     if e.type in evtypes)[:]
    sessions = {
        'days': [
            {'date': d.strftime('%d-%m-%Y'),
             'events': map(
                 event2dict,
                 model.Event.select(lambda e:
                                 e.type in evtypes and
                                 e.from_.date()==d) )
            }
            for d in days]
        }
    return sessions

for funcname, typenames in API_SESSION_TYPES:
    def _func(typenames = typenames):
        return events_by_types(typenames)
    _func.__name__ = _func.func_name = funcname
    locals()[funcname] = public(_func)


if not model.initialized():
    if not op.isfile(options.pyconil2016_db):
        model.init(options.pyconil2016_db, initialize=True, debug=options.debug_sql)
        model.populate_from_json()
    else:
        model.init(options.pyconil2016_db, debug=options.debug_sql)
