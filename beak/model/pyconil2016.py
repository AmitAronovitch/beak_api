# Designed via web interface: https://editor.ponyorm.com/user/amitar/pyconil_2016_test/designer
# Notes (for Speaker table):
# * email contains nulls (not empty strings, nullable=True)
# * on firstName we need autostrip=False,

import logging
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

# initialization

def init(filename, initialize=False, debug=False):
    logging.debug('initializing pyconil2016 model, filename={0}, init={1}, debug={2}'.format(
        filename, initialize, debug))
    if debug:
        sql_debug(True)
    db.bind(provider='sqlite', filename=filename, create_db=initialize)
    db.generate_mapping(create_tables=initialize)

def initialized():
    return db.provider is not None


def _ref_from_id(row, field, table):
    if row[field]:
        row[field] = table[row[field]]
    else:
        del row[field]

@db_session
def populate_from_data(data):
    for table in ['Level', 'Type', 'Track', 'Location', 'Speaker']:
        logging.debug('populating {0} table'.format(table))
        rows = [globals()[table](**x) for x in data[table]]
    
    logging.debug('populating Event table')
    rows = []
    for e in data['Event']:
        e['type'] = Type[e['type']]
        _ref_from_id(e, 'track', Track)
        _ref_from_id(e, 'experienceLevel', Level)        
        e["speakers"] = [Speaker[s] for s in e["speakers"]]
        rows.append(Event(**e))
