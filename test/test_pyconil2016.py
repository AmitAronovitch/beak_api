import os, os.path as op, json
import pytest
import beak.api.pyconil2016 as api
import beak.api.pyconil2016_old as oldapi

apidir = op.abspath(op.split(api.__file__)[0])
datadir = op.abspath(op.join(apidir, '..','data', 'pyconil2016'))

datatest = pytest.mark.skipif(
    not op.isdir(datadir), reason='Requires data submodule')

@datatest
def test_data():
    for cmd in api.__all__:
        data = getattr(api, cmd)()
        jdata = json.load(open(
            op.join(datadir, '.'.join([cmd, 'json']))
        ))
        assert data==jdata
