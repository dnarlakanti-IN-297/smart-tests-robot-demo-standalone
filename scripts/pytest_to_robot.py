#!/usr/bin/env python3
"""
Convert pytest format back to Robot Framework format for test execution.
"""
import sys


def from_pytest_format(pytest_name):
    """
    Convert pytest format back to Robot Framework format.

    Input:
      "tests.robot.api.auth::test_register_new_user_successfully"
      "tests.robot.integration.project workflow::test_issue_priority_and_type_combinations_workflow"

    Output:
      "Api.Auth.Register New User Successfully"
      "Integration.Project Workflow.Issue Priority And Type Combinations Workflow"
    """
    if "::" not in pytest_name:
        return pytest_name

    file_part, method_part = pytest_name.split("::", 1)

    # tests.robot.api.auth -> Api.Auth
    # tests.robot.integration.project workflow -> Integration.Project Workflow
    if file_part.startswith("tests.robot."):
        suite_path = file_part[12:]  # Remove "tests.robot."
        # Handle spaces in suite names (e.g., "project workflow")
        # Split by dots, then capitalize each word (including words within spaces)
        suite_parts = []
        for part in suite_path.split("."):
            # Capitalize each word in multi-word parts
            capitalized = " ".join(word.capitalize() for word in part.split())
            suite_parts.append(capitalized)
        suite_name = ".".join(suite_parts)
    else:
        suite_name = file_part

    # test_register_new_user_successfully -> Register New User Successfully
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
