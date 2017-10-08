from . import pyconil2016_static as static
from ..model import load as model_load
from ..utils import public, rename

model = model_load('pyconil2016')

API_STATIC = 'checkUpdates', 'getInfo', 'getSettings', 'getPOI'

API_TABLES = [
    ('getLevels', 'levels'),
    ('getLocations', 'locations'),
    ('getSpeakers', 'speakers'),
    ('getTypes', 'types'),
    ('getTracks', 'tracks'),
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
def getSessions():
    days = model.select(e.from_.date() for e in model.Event)[:]
    days_data = []
    for day in days:
        days_data.append({
            'date': day.strftime('%d-%m-%Y'),
            'events': list(map(
                event2dict,
                model.Event.select(lambda e: e.from_.date() == day)
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
                                   e.from_.date() == day)
            ))
        })
    return {'days': days_data}


for funcname, typenames in API_SESSION_TYPES:
    @public
    @rename(funcname, locals())
    def _func(typenames=typenames):
        return events_by_types(typenames)


    del _func
