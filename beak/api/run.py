#!/usr/bin/env python
import bottle

from ..config import options

if __name__ == '__main__':
    bottle.run(host=options.host, port=options.port)
