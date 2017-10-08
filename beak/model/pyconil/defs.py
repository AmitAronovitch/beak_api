# Designed via web interface: https://editor.ponyorm.com/user/amitar/pyconil_generic/designer
# (when updating, remove the generate_mapping() call at the bottom)
from datetime import datetime
from datetime import timedelta

from pony.orm import *

db = Database()


class SessionType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    sessions = Set('Session')


class Track(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    event = Required('Event')
    sessions = Set('Session')


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    tracks = Set(Track)


class Location(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    sessions = Set('Session')


class Session(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    abstract = Optional(str)
    time = Required(datetime)
    duration = Required(timedelta)
    session_type = Required(SessionType)
    speakers = Set('Speaker')
    location = Required(Location)
    track = Required(Track)
    video = Optional(str)
    image_url = Optional(str)


class Speaker(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    bio = Optional(str)
    image_url = Optional(str)
    twitter = Optional(str)
    github = Optional(str)
    webpage = Optional(str)
    sessions = Set(Session)
