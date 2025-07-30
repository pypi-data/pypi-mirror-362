import os

# NOTE
# This file assumes two workers, the first half of tests should be
# in worker-1 and the second half in worker-2.


def test_1():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '1'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_2():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '1'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_3():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '1'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_4():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '1'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_5():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '1'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_6():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '2'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_7():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '2'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_8():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '2'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'


def test_9():
    if os.environ.get('TF_BUILD'):
        assert os.environ['SYSTEM_JOBPOSITIONINPHASE'] == '2'
        assert os.environ['SYSTEM_TOTALJOBSINPHASE'] == '2'
