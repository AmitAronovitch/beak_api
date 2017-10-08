import json
import os.path as op

import pytest

import beak.api.pyconil2016 as api
import beak.api.pyconil2016_old as oldapi

apidir = op.abspath(op.split(api.__file__)[0])
datadir = op.abspath(op.join(apidir, '..', 'data', 'pyconil2016'))

datatest = pytest.mark.skipif(
    not op.isdir(datadir), reason='Requires data submodule')


@datatest
def test_data():
    for cmd in api.__all__:
        data = getattr(api, cmd)()
        jdata = json.load(open(
            op.join(datadir, '.'.join([cmd, 'json']))
        ))
        assert data == jdata


@datatest
def test_old_data():
    for cmd in oldapi.__all__:
        data = getattr(oldapi, cmd)()
        jdata = json.load(open(
            op.join(datadir + '_old', '.'.join([cmd, 'js']))
        ))
        assert data == jdata
