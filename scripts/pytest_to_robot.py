#!/usr/bin/env python3
"""
Convert pytest format back to Robot Framework test name for --test argument.
Robot Framework --test expects ONLY the test name, not the full qualified name.
"""
import sys


def from_pytest_format(pytest_name):
    """
    Convert pytest format to Robot Framework test name.

    Input:
      "tests.robot.integration.issue_lifecycle::test_bug_fix_workflow_with_type_and_priority"

    Output:
      "Bug Fix Workflow With Type And Priority"  (just the test name)
    """
    if "::" not in pytest_name:
        return pytest_name

    _, method_part = pytest_name.split("::", 1)

    # test_bug_fix_workflow_with_type_and_priority -> Bug Fix Workflow With Type And Priority
    if method_part.startswith("test_"):
        method_part = method_part[5:]  # Remove "test_"
    test_name = " ".join(word.capitalize() for word in method_part.split("_"))

    return test_name


if __name__ == '__main__':
    for line in sys.stdin:
        pytest_name = line.strip()
        if pytest_name:
            robot_name = from_pytest_format(pytest_name)
            print(robot_name)
