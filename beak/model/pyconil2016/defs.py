# Designed via web interface: https://editor.ponyorm.com/user/amitar/pyconil_2016_test/designer
# Notes (for Speaker table):
# * email contains nulls (not empty strings, nullable=True)
# * on firstName we need autostrip=False,

from datetime import datetime

from pony.orm import *

db = Database()


class Speaker(db.Entity):
    speakerId = PrimaryKey(int, auto=True)
    firstName = Required(str, autostrip=False)
    lastName = Required(str)
    avatarImageURL = Optional(str)
    organizationName = Optional(str)
    jobTitle = Optional(str)
    characteristic = Optional(str)
    email = Optional(str, nullable=True)
    twitterName = Optional(str)
    webSite = Optional(str)
    order = Optional(float)
    deleted = Required(bool, default=False)
    _events = Set('Event')


class Event(db.Entity):
    eventId = PrimaryKey(int, auto=True)
    from_ = Required(datetime)
    to = Required(datetime)
    name = Required(str)
    type = Required('Type')
    place = Optional(str)
    text = Optional(str)
    track = Optional('Track')
    experienceLevel = Optional('Level')
    speakers = Set(Speaker)
    version = Optional(str)
    order = Optional(float)
    link = Optional(str)
    deleted = Required(bool, default=False)


class Level(db.Entity):
    levelId = PrimaryKey(int, auto=True)
    levelName = Required(str)
    order = Optional(float)
    deleted = Required(bool, default=False)
    _events = Set(Event)


class Track(db.Entity):
    trackId = PrimaryKey(int, auto=True)
    trackName = Required(str)
    order = Optional(float)
    deleted = Required(bool, default=False)
    _events = Set(Event)


class Type(db.Entity):
    typeId = PrimaryKey(int, auto=True)
    typeName = Required(str)
    typeIconURL = Optional(str)
    order = Optional(float)
    deleted = Required(bool, default=False)
    _events = Set(Event)


class Location(db.Entity):
    locationId = PrimaryKey(int, auto=True)
    locationName = Required(str)
    longitude = Optional(float)
    latitude = Optional(float)
    address = Optional(str)
    order = Optional(float)
    deleted = Required(bool, default=False)
