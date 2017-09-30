import logging
from .defs import *

def _ref_from_id(row, field, table):
    if row[field]:
        row[field] = table[row[field]]
    else:
        del row[field]

@db_session
def populate(data):
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
