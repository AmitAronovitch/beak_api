import logging

from .defs import *


# functions for later refactoring:
#  should be useful for automating the populate() method
#  (based on data conventions)

# def entity_relations(entity):
#    return [
#        prop for prop in entity._base_attrs_ + entity._new_attrs_
#        if isinstance(prop.py_type, (str, core.EntityMeta)) ]

# initialization

def _ref_from_id(row, field, table):
    if row[field]:
        row[field] = table[row[field]]
    else:
        del row[field]


@db_session
def populate(data):
    for table in ['Event', 'Speaker', 'SessionType', 'Location']:
        logging.debug('populating {0} table'.format(table))
        rows = [globals()[table](**x) for x in data[table]]

    logging.debug('populating Track table')
    tracks = []
    for d in data['Track']:
        _ref_from_id(d, 'event', Event)
        tracks.append(Track(**d))

    logging.debug('populating Session table')
    rows = []
    for d in data['Session']:
        _ref_from_id(d, 'session_type', SessionType)
        _ref_from_id(d, 'location', Location)
        _ref_from_id(d, 'track', Track)
        d["speakers"] = [Speaker[s] for s in d["speakers"]]
        rows.append(Session(**d))
