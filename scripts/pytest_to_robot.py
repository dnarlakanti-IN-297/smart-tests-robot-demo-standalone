#!/usr/bin/env python3
"""
Convert pytest format back to Robot Framework format for test execution.
"""
import sys


def from_pytest_format(pytest_name):
    """
    Convert pytest format back to Robot Framework format.

    Input:
      "tests.robot.integration.issue_lifecycle::test_bug_fix_workflow_with_type_and_priority"

    Output:
      "Integration.Issue Lifecycle.Bug Fix Workflow With Type And Priority"
    """
    if "::" not in pytest_name:
        return pytest_name

    file_part, method_part = pytest_name.split("::", 1)

    # tests.robot.integration.issue_lifecycle -> Integration.Issue Lifecycle
    if file_part.startswith("tests.robot."):
        suite_path = file_part[12:]  # Remove "tests.robot."
        # Split by dots and convert: issue_lifecycle -> Issue Lifecycle
        suite_parts = []
        for part in suite_path.split("."):
            # Convert underscores to spaces and capitalize: issue_lifecycle -> Issue Lifecycle
            capitalized = " ".join(word.capitalize() for word in part.split("_"))
            suite_parts.append(capitalized)
        suite_name = ".".join(suite_parts)
    else:
        suite_name = file_part

    # test_bug_fix_workflow_with_type_and_priority -> Bug Fix Workflow With Type And Priority
    if method_part.startswith("test_"):
        method_part = method_part[5:]  # Remove "test_"
    test_name = " ".join(word.capitalize() for word in method_part.split("_"))

    return f"{suite_name}.{test_name}"


if __name__ == '__main__':
    for line in sys.stdin:
        pytest_name = line.strip()
        if pytest_name:
            robot_name = from_pytest_format(pytest_name)
            print(robot_name)
