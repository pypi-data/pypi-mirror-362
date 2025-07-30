# -*- coding: utf-8 -*-

import os
import pytest


def grouper(items, total_groups: int):
    """
    >>> grouper([1,2,3,4,5,6,7,8], 1)
    [[1, 2, 3, 4, 5, 6, 7, 8]]

    >>> grouper( [1,2,3,4,5,6,7,8], 2 )
    [[1, 2, 3, 4], [5, 6, 7, 8]]

    >>> grouper([1,2,3,4,5,6,7,8], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8]]

    >>> grouper([1,2,3,4,5,6,7,8], 4)
    [[1, 2], [3, 4], [5, 6], [7, 8]]

    >>> grouper([1,2,3,4,5,6,7,8], 5)
    [[1, 2], [3, 4], [5, 6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8], 6)
    [[1, 2], [3, 4], [5], [6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8], 7)
    [[1, 2], [3], [4], [5], [6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8], 8)
    [[1], [2], [3], [4], [5], [6], [7], [8]]

    >>> grouper([1,2,3,4,5,6,7,8, 9], 4)
    [[1, 2, 3], [4, 5], [6, 7], [8, 9]]
    """
    if total_groups <= 0:
        raise ValueError(f"total_groups should be bigger than zero but got {total_groups}")
    if total_groups >= len(items):
        return [[item] for item in items]

    chunk_size = len(items) // total_groups
    remainder = len(items) % total_groups

    groups = []
    start = 0

    for i in range(total_groups):
        # First 'remainder' groups get an extra item
        current_size = chunk_size + (1 if i < remainder else 0)
        groups.append(items[start:start + current_size])
        start += current_size

    return groups


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    if not os.environ.get("TF_BUILD"):
        print(
            "pytest-azure-devops installed but not in azure devops (plugin disabled). "
            "To run plugin either run in tests in CI azure devops "
            "or set environment variables "
            "TF_BUILD, SYSTEM_TOTALJOBSINPHASE and "
            "SYSTEM_JOBPOSITIONINPHASE."
        )
        return

    total_agents = int(os.environ.get("SYSTEM_TOTALJOBSINPHASE", 1))
    agent_index = int(os.environ.get("SYSTEM_JOBPOSITIONINPHASE", 1)) - 1

    agent_tests = grouper(items, total_agents)[agent_index]

    print(
        f"Agent nr. {agent_index + 1} of {total_agents} "
        f"selected {len(agent_tests)} of {len(items)} tests "
        "(other filters might apply afterwards, e.g. pytest marks)"
    )

    items[:] = agent_tests


if __name__ == "__main__":
    import doctest

    print(doctest.testmod(raise_on_error=True))
