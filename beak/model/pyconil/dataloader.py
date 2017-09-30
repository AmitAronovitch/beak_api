import os.path as op
import logging, json
import datetime as dt

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

def load():
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
    by_name = dict( (x['name'],x) for x in speakers )
    assert len(by_name) == len(speakers)
    
    names_by_id = {}
    for session in sessions:
        for name, link in session['speakers']:
            sid = int(link.split('/')[-1])
            names_by_id.setdefault(sid, set()).add(name)

    speaker_by_id = {}
    for sid, names in names_by_id.items():
        assert len(names)==1
        name = next(iter(names))
        assert name in by_name
        speaker_by_id[sid] = by_name[name]

    # generated entities
    data = {}
    
    locs = sorted(set(x['location'] for x in sessions))
    loc_ids = dict( (name, i+1) for i,name in enumerate(locs) )
    data['Location'] = [{'id':loc_ids[x], 'name':x} for x in locs]

    types = sorted(set(type_convert_dict.get(x['type'], x['type'])
                       for x in sessions) )
    type_ids = dict( (t, i+1) for i,t in enumerate(types))
    for aliases, t in type_conversions:
        for a in aliases:
            type_ids[a] = type_ids[t]
    data['SessionType'] = [{'id':type_ids[x], 'name':x} for x in types]

    data['Event'] = [{'id':1, 'name':'PyCon Israel 2017'}]
    
    tracks = sorted(set(x['track'] for x in sessions))
    track_ids = dict( (t, i+1) for i,t in enumerate(tracks) )
    data['Track'] = [{'id': track_ids[x], 'name':x, 'event':1}
                     for x in tracks]
    
    speaker_ids = dict( (s['name'], i+1) for i,s in enumerate(speakers) )
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
    session_ids = dict( (s['sessionId'], i+1) for i,s in enumerate(sessions) )
    for session in sessions:
        d = {}
        _limited_update(d, session, {'title', 'video'})
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
