import warnings, logging
import os.path as op, json
from dateutil.parser import parse
from ..config import options
from ..model import pyconil2016 as model
from . import pyconil2016_static as static

__all__ = []

# define decorators

def public(func):
    __all__.append(func.__name__)
    return func

def rename(name, scope=None):
    def renamed(func):
        func.__name__ = name
        if scope is not None:
            scope[name] = func
        return func
    return renamed

API_STATIC = 'checkUpdates', 'getInfo', 'getSettings', 'getPOI'

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


for funcname in API_STATIC:
    @public
    @rename(funcname, locals())
    def _func(funcname=funcname):
        return getattr(static, funcname)
    
    del _func

# Level, Type, Location, Speaker, Track

for funcname, table in API_TABLES:
    entity_name = table[:-1].capitalize()
    
    @public
    @rename(funcname, locals())
    @model.db_session
    def _func(table=table, entity_name=entity_name):
        return {table: [x.to_dict()
                        for x in getattr(model, entity_name).select()]}
    
    del _func

# Queries on the Event table
    
def emulate_old_format(data):
    "convert Event's json to old data format"
    # from and to had also "+0000" (but that was just wrong)
    data['from'] = data['from'] + '+0000'
    data['to'] = data['to'] + '+0000'
    # original API did not have the youtube link
    data['link'] = ''

def event2dict(e):
    d = e.to_dict()
    if d['experienceLevel'] is None:
        d['experienceLevel'] = 0
    d['from'] = d.pop('from_').isoformat()
    d['to'] = d['to'].isoformat()
    d['speakers'] = sorted([x.speakerId for x in e.speakers])
    return d

@public
@model.db_session
def getSessions(test=False):
    days = model.select(e.from_.date() for e in model.Event)[:]
    days_data = []
    for day in days:
        days_data.append({
            'date': day.strftime('%d-%m-%Y'),
             'events': list(map(
                 event2dict,
                 model.Event.select(lambda e: e.from_.date()==day)
             ))
        })
    return {'days': days_data}


@model.db_session
def events_by_types(type_names):
    evtypes = model.Type.select(lambda t: t.typeName in type_names)
    days = model.select(e.from_.date() for e in model.Event
                     if e.type in evtypes)[:]
    days_data = []
    for day in days:
        days_data.append({
            'date': day.strftime('%d-%m-%Y'),
            'events': list(map(
                event2dict,
                model.Event.select(lambda e:
                                   e.type in evtypes and
                                   e.from_.date()==day)
            ))
        })
    return {'days': days_data}

for funcname, typenames in API_SESSION_TYPES:
    @public
    @rename(funcname, locals())
    def _func(typenames = typenames):
        return events_by_types(typenames)

    del _func

# initialization stuff

def load_json_data():
    thisdir = op.abspath(op.split(__file__)[0])
    jsondir = op.abspath(op.join(thisdir,'..','data','pyconil2016'))
    logging.debug('checking for data directory at ' + jsondir)
    if not op.isdir(jsondir):
        return
    
    logging.debug('loading data from json files')
    data = {}
    for cmd, key in API_TABLES:
        jdata = json.load(open(op.join(jsondir, cmd+'.json')))
        table = key[:-1].capitalize()
        data[table] = jdata[key]
    
    days = json.load(open(op.join(jsondir, 'getSessions.json')))['days']
    events =  sum([day['events'] for day in days], [])
    for e in events:
        e["from_"] = parse(e.pop("from"))
        e["to"] = parse(e["to"])
    data['Event'] = events
    return data

# initialize model if required

if not model.initialized():
    if op.isfile(options.pyconil2016_db):
        model.init(options.pyconil2016_db, debug=options.debug_sql)
    else:
        model.init(options.pyconil2016_db, initialize=True, debug=options.debug_sql)
        data = load_json_data()
        if data:
            model.populate_from_data(data)
        else:
            warnings.warn('pyconil2016: Missing data directory. DB will remain empty')
