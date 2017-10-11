from ..utils import public, rename
from . import pyconil2016 as api

cmd_suffix = '.js'


# private funcs

def _emulate_old_event(event):
    "convert Event's json to old event format"
    # from and to had also "+0000" (but that was just wrong)
    event['from'] = event['from'] + '+0000'
    event['to'] = event['to'] + '+0000'
    # original API did not have the youtube link
    event['link'] = ''


def _fix_sessions_output(data):
    for day in data['days']:
        for event in day['events']:
            _emulate_old_event(event)
    return data


# export funcs which remain the same

for name in api.API_STATIC + \
        ('getLevels', 'getSpeakers', 'getTypes', 'getTracks', 'getBofs'):
    @public
    @rename(name, locals())
    def _f(name=name):
        return getattr(api, name)()


# modified funcs

@public
def getLocations():
    data = api.getLocations()
    for loc in data['locations']:
        loc['longitude'] = '{0:.6f}'.format(loc['longitude'])
        loc['latitude'] = '{0:.6f}'.format(loc['latitude'])
    return data


@public
def getSessions():
    return _fix_sessions_output(api.getSessions())


@public
def getSocialEvents():
    return _fix_sessions_output(api.getSocialEvents())
