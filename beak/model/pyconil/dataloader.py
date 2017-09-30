import os.path as op
import logging, json
import datetime as dt
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from ..pyconil2016.dataloader import load as load_2016

#types: 
#   'Talk', 'Keynote', 'Workshop', 'Social', 'Break'

type_conversions = [
    (['Coffee'], 'Break'),
    (['Frontal'], 'Talk'),
    (['Lunch'], 'Social')
]

type_convert_dict = {}
for aliases, t in type_conversions:
    for a in aliases:
        type_convert_dict[a] = t


def _limited_update(d, other, limit):
    for k in other:
        if k in limit:
            if other[k] is not None:
                d[k]=other[k]

def _url2video(url):
    o = urlparse(url)
    if o.netloc != 'www.youtube.com':
        return url
    else:
        return 'youtube:'+o.path.split('/')[-1]

def load_2017(initial_ids={}, old_speakers={}):
    
    def firstid(table):
        return initial_ids.get(table,1)
    
    thisdir = op.abspath(op.split(__file__)[0])
    jsondir = op.abspath(op.join(thisdir,'..','..','data','pyconil2017'))
    logging.debug('checking for data directory at ' + jsondir)
    if not op.isdir(jsondir):
        return
    
    logging.debug('loading data from json files')
    sessions = json.load(open(op.join(jsondir, 'pyconil2017_agenda.json')))['sessions']
    session_by_name = dict( (x['sessionId'], x) for x in sessions )
    
    speakers = json.load(open(op.join(jsondir, 'pyconil2017_speakers.json')))['speakers']
    
    # speakers table has no ids, try to match ids from sessions
    # by using the names.
    #by_name = dict( (x['name'],x) for x in speakers )
    #assert len(by_name) == len(speakers)
    
    #names_by_id = {}
    #for session in sessions:
    #    for name, link in session['speakers']:
    #        sid = int(link.split('/')[-1])
    #        names_by_id.setdefault(sid, set()).add(name)

    #speaker_by_id = {}
    #for sid, names in names_by_id.items():
    #    assert len(names)==1
    #    name = next(iter(names))
    #    assert name in by_name
    #    speaker_by_id[sid] = by_name[name]

    # generated entities
    data = {}
    
    locs = sorted(set(x['location'] for x in sessions))
    loc_ids = dict( (name, i+firstid('Location'))
                    for i,name in enumerate(locs) )
    data['Location'] = [{'id':loc_ids[x], 'name':x} for x in locs]

    types = sorted(set(type_convert_dict.get(x['type'], x['type'])
                       for x in sessions) ) + ['Administrative']
    type_ids = dict( (t, i+firstid('SessionType')) for i,t in enumerate(types))
    for aliases, t in type_conversions:
        for a in aliases:
            type_ids[a] = type_ids[t]
    data['SessionType'] = [{'id':type_ids[x], 'name':x} for x in types]

    data['Event'] = [{'id':firstid('Event'), 'name':'PyCon Israel 2017'}]
    
    tracks = sorted(set(x['track'] for x in sessions))
    track_ids = dict( (t, i+firstid('Track')) for i,t in enumerate(tracks) )
    data['Track'] = [{'id': track_ids[x], 'name':x, 'event':firstid('Event')}
                     for x in tracks]

    speaker_ids = {}; i=firstid('Speaker')
    for s in speakers:
        name = s['name']
        if name in old_speakers:
            speaker_ids[name] = old_speakers[name]
        else:
            speaker_ids[name] = i
            i = i+1
    
    data['Speaker'] = []
    for speaker in speakers:
        d = {}
        _limited_update(d, speaker,
                        {'name','bio','twitter','github'})
        
        d['id'] = speaker_ids[speaker['name']]
        if speaker['image']:
            d['image_url'] = speaker['image']
        if speaker['linkedin']:
            d['webpage'] = speaker['linkedin']
        data["Speaker"].append(d)
    
    data['Session'] = []
    session_ids = dict( (s['sessionId'], i+firstid('Session')) for i,s in enumerate(sessions) )
    for session in sessions:
        d = {}
        _limited_update(d, session, {'title', 'video'})
        if d.get('video'):
            d['video'] = _url2video(d['video'])
        #d['image_url'] = None
        if session['body']:
            d['abstract'] = session['body']
        d['id'] = session_ids[session['sessionId']]
        d['time'] = dt.datetime.strptime(session['time'], '%a, %m/%d/%Y - %H:%M')
        assert session['duration'].endswith('min')
        d['duration'] = dt.timedelta(minutes=int(session['duration'][:-3]))
        
        d['session_type'] = type_ids[session['type']]
        d['speakers'] = [
            speaker_ids[name]
            for name,link in session['speakers']
        ]
        d['location'] = loc_ids[session['location']]
        d['track'] = track_ids[session['track']]
        #TODO: link to talk pdf/zip!
        data['Session'].append(d)
    
    return data

# TODO
# Model improvements
# * fix/unify video link
# * Add to model:
#     ExperienceLevel
#     Session.slides
#     
# merge: Type -> SessionType (add new one: Administrative)
# merge: Speaker -> Speaker
# import: Event->Session
_new_typenames = {
    'Speech': 'Talk',
    'Keynote': 'Keynote',
    'Coffee break': 'Break',
    'Lunch': 'Social',
    'Registration': 'Administrative',
    'After party': 'Social',
    'Movie': 'Social',
}

class Convertor:
    "assists in converting and merging 2016 data"
    
    def __init__(self, old, new):
        self.old = old
        newids = {x['name']: x['id'] for x in new['SessionType']}
        self.new_typeid = {
            x['typeId']: newids.get(_new_typenames.get(x['typeName']))
            for x in old['Type']
        }
        old_s = [x['firstName']+x['lastName'] for x in old['Speaker']]
        new_s = [x['name'] for x in new['Speaker']]
        common = set(old_s) & set(new_s)
        self.common_speakers = {
            x: old['Speaker'][old_s.index(x)]['speakerId']
            for x in common
        }
        
        max_ids = {}
        for table in old:
            idname = table.lower()+'Id'
            max_ids[table] = max( x[idname] for x in old[table] )
        self.max_old_id = max_ids
    
    def initial_2017_ids(self):
        inits = {
            'Event': 1+1,
            'Session': self.max_old_id['Event']+1,
            'Speaker': self.max_old_id['Speaker']+1,
            'Location': 1+1,
            'Track': self.max_old_id['Track']+1+1
        }
        return inits

    def old_data(self):
        data = {}
        data['Event'] = [dict(id=1, name='PyCon Israel 2016')]
        data['Location'] = [dict(
            id=1, name=self.old['Location'][0]['locationName'] )]
        tracks = []
        for t in self.old['Track']:
            tracks.append(dict(
                id = t['trackId'], name=t['trackName'], event=1))
        common_track_id = self.max_old_id['Track']+1
        tracks.append(dict(
            id = common_track_id,
            name = 'Common', event=1
        ))
        data['Track'] = tracks
        data['SessionType'] = []
        speakers = []
        for s in self.old['Speaker']:
            name = s['firstName']+s['lastName']
            # common speakers' data will be taken from the new data
            # (but with old ids)
            if name in self.common_speakers: continue
            d = dict(
                id = s['speakerId'], name=name,
                bio = s['characteristic'],
            )
            if s.get('avatarImageURL'):
                d['image_url'] = s['avatarImageURL']
            if s.get('twitterName'):
                d['twitter'] = s['twitterName']
            if s.get('webSite'):
                d['webpage'] = s['webSite']
            speakers.append(d)
        data['Speaker'] = speakers
        
        sessions = []
        for e in self.old['Event']:
            d = dict(
                id = e['eventId'], time = e['from_'],
                duration = e['to']-e['from_'],
                title = e['name'],
                abstract = e['text'],
                session_type = self.new_typeid[e['type']],
                speakers = e['speakers'],
                location = 1,
                track = common_track_id if e['track'] is None else e['track'],
            )
            if e.get('link'):
                d['video'] = 'youtube:'+e['link']
            sessions.append(d)
        data['Session'] = sessions
        
        return data

def load():
    old = load_2016()
    new = load_2017()
    c = Convertor(old, new)
    new = load_2017(c.initial_2017_ids(), c.common_speakers)
    
    data = c.old_data()
    for key in data:
        data[key].extend(new[key])
    return data
