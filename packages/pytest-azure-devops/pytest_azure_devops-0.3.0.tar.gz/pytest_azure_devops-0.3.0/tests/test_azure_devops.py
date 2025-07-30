# -*- coding: utf-8 -*-

def test_azure_devops_with_pytest_mark(testdir, monkeypatch):
    monkeypatch.setenv('TF_BUILD', '1')
    monkeypatch.setenv('SYSTEM_TOTALJOBSINPHASE', '3')
    monkeypatch.setenv('SYSTEM_JOBPOSITIONINPHASE', '2')

    testdir.makeini("""
    [pytest]
    markers =
        asubset: marks tests as asubset (deselect with '-m "not asubset"')
    """)
    testdir.makepyfile("""
        import pytest

        def test_1(): ...
        def test_2(): ...
        def test_3(): ...
        @pytest.mark.asubset
        def test_4(): ...
        @pytest.mark.asubset
        def test_5(): ...
        def test_6(): ...
        def test_7(): ...
        def test_8(): ...
        @pytest.mark.asubset
        def test_9(): ...
    """)

    result = testdir.runpytest('-m asubset', '-v')

    result.stdout.fnmatch_lines([
        # Marks are filtered before the plugin can decide what tests
        # to execute, thus 3 tests only to select from.
        '*Agent nr. 2 of 3 selected 1 of 3 tests*',
        # worker 2 selects only test 5
        '*::test_5 PASSED*',
        # 6 deselect: tests that does not have `asubset` mark
        '*1 passed, 6 deselected*',
    ])

    assert result.ret == 0

    result = testdir.runpytest('-m not asubset', '-v')

    result.stdout.fnmatch_lines([
        # Marks are filtered before the plugin can decide what tests
        # to execute, thus 6 tests only to select from.
        '*Agent nr. 2 of 3 selected 2 of 6 tests*',
        # worker 2 selects only test 3 & 6
        '*::test_3 PASSED*',
        '*::test_6 PASSED*',
        # 6 deselected: test that have `asubset` mark
        '*2 passed, 3 deselected*',
    ])

    assert result.ret == 0


def test_azure_devops_group_selection(testdir, monkeypatch):
    monkeypatch.setenv('TF_BUILD', '1')
    monkeypatch.setenv('SYSTEM_TOTALJOBSINPHASE', '3')
    monkeypatch.setenv('SYSTEM_JOBPOSITIONINPHASE', '1')

    testdir.makepyfile("""
        # group 1
        def test_1(): ...
        def test_2(): ...
        def test_3(): ...

        # group 2
        def test_4(): ...
        def test_5(): ...
        def test_6(): ...

        # group 3
        def test_7(): ...
        def test_8(): ...
        def test_9(): ...
    """)

    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*Agent nr. 1 of 3 selected 3 of 9 tests*',
        '*::test_1 PASSED*',
        '*::test_2 PASSED*',
        '*::test_3 PASSED*',
        '*3 passed*',
    ])

    assert result.ret == 0


def test_not_in_azure_devops(testdir, monkeypatch):
    monkeypatch.setenv('TF_BUILD', '')

    testdir.makepyfile("""
        def test_1(): ...
        def test_2(): ...
        def test_3(): ...
        def test_4(): ...
        def test_5(): ...
        def test_6(): ...
        def test_7(): ...
        def test_8(): ...
        def test_9(): ...
    """)

    result = testdir.runpytest('-v')

    result.stdout.fnmatch_lines([
        '*pytest-azure-devops installed but not in azure devops (plugin disabled).*',
        '*::test_1 PASSED*',
        '*::test_2 PASSED*',
        '*::test_3 PASSED*',
        '*::test_4 PASSED*',
        '*::test_5 PASSED*',
        '*::test_6 PASSED*',
        '*::test_7 PASSED*',
        '*::test_8 PASSED*',
        '*::test_9 PASSED*',
        '*9 passed*',
    ])

    assert result.ret == 0
