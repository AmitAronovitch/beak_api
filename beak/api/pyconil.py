from ..utils import public
from ..model import load as model_load

model = model_load('pyconil')


def session2dict(s):
    d = s.to_dict()
    d['time'] = d['time'].strftime('%Y-%m-%d %H:%M')
    d['duration'] = str(d['duration'])
    d['location'] = model.Location[d['location']].name
    d['session_type'] = model.SessionType[d['session_type']].name
    #d['track'] = model.Track[d['track']].name
    return d

def get_by_id(entity, id, default=None):
    try:
        return entity[id]
    except model.ObjectNotFound:
        return default

@public
@model.db_session
def events():
    return {
        'events': [x.to_dict() for x in model.Event.select()]
    }


@public
@model.db_session
def event_tracks(event_id):
    event = get_by_id(model.Event, event_id)
    if event is None: return {'tracks':[]}
    return {'tracks':[x.to_dict() for x in event.tracks]}

@public
@model.db_session
def event_sessions(event_id):
    event = get_by_id(model.Event, event_id)
    if event is None: return {'sessions':[]}
    sessions = event.tracks.sessions.order_by(model.Session.time)
    return {'sessions':[session2dict(x) for x in sessions]}

@public
@model.db_session
def event_speakers(event_id):
    event = get_by_id(model.Event, event_id)
    if event is None: return {'speakers':[]}
    sessions = event.tracks.sessions
    query = model.select(
        speaker
        for speaker in model.Speaker for s in speaker.sessions
        if s in sessions)
    return {'speakers': [x.to_dict() for x in query]}


@public
@model.db_session
def track_sessions(track_id):
    track = get_by_id(model.Track, track_id)
    if track is None: return {'sessions':[]}
    sessions = track.sessions.order_by(model.Session.time)
    return {'sessions': [session2dict(x) for x in sessions]}

@public
@model.db_session
def track_speakers(track_id):
    track = get_by_id(model.Track, track_id)
    if track is None: return {'speakers':[]}
    query = model.select(
        speaker
        for speaker in model.Speaker for session in speaker.sessions
        if session in track.sessions)
    return {'speakers': [x.to_dict() for x in query]}


@public
@model.db_session
def speaker_sessions(speaker_id):
    speaker = get_by_id(model.Speaker, speaker_id)
    if speaker is None: return {'sessions':[]}
    sessions = speaker.sessions.order_by(model.Session.time)
    return {'sessions': [session2dict(x) for x in sessions]}

@public
@model.db_session
def session_speakers(session_id):
    session = get_by_id(model.Session, session_id)
    if session is None: return {'speakers': []}
    speakers = session.speakers
    return {'speakers': [x.to_dict() for x in speakers]}


@public
@model.db_session
def all_speakers():
    return {
        'speakers': [x.to_dict() for x in model.Speaker.select()]
    }

@public
@model.db_session
def all_sessions():
    return {
        'sessions': [session2dict(x) for x in model.Session.select().order_by(model.Session.time)]
    }

