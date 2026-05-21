#!/usr/bin/env python3
"""
Transform Robot Framework JUnit XML to pytest-compatible format for Smart Tests.
This allows Smart Tests to understand Robot Framework test results.
"""
import sys
import xml.etree.ElementTree as ET
import re


def to_pytest_format(classname, test_name):
    """
    Convert Robot Framework test to pytest module format.

    Input:
      classname: "Robot.Integration.Issue Lifecycle"
      test_name: "Bug Fix Workflow With Type And Priority"

    Output:
      "tests.robot.integration.issue_lifecycle::test_bug_fix_workflow_with_type_and_priority"
    """
    # Remove "Robot." prefix
    if classname.startswith("Robot."):
        suite_path = classname[6:]  # Remove "Robot."
    else:
        suite_path = classname

    # Convert suite path to module path: "Integration.Issue Lifecycle" -> "tests.robot.integration.issue_lifecycle"
    # Use dots for module format, convert to lowercase, replace spaces with underscores
    suite_parts = suite_path.split(".")
    file_parts = [re.sub(r'\s+', '_', part.lower()) for part in suite_parts]
    file_path = "tests.robot." + ".".join(file_parts)

    # Convert test name to pytest format
    method_name = "test_" + re.sub(r'[^a-zA-Z0-9]+', '_', test_name).lower().strip('_')

    return f"{file_path}::{method_name}"


def from_pytest_format(pytest_name):
    """
    Convert pytest format back to Robot Framework format.

    Input:
      "tests.robot.api.auth::test_register_new_user_successfully"

    Output:
      classname: "Robot.Api.Auth"
      test_name: "Register New User Successfully" (approximation)
    """
    if "::" not in pytest_name:
        return None, None

    file_part, method_part = pytest_name.split("::", 1)

    # tests.robot.api.auth -> Api.Auth
    if file_part.startswith("tests.robot."):
        suite_path = file_part[12:]  # Remove "tests.robot."
        # api.auth -> Api.Auth
        suite_parts = [p.capitalize() for p in suite_path.split(".")]
        classname = "Robot." + ".".join(suite_parts)
    else:
        classname = file_part

    # test_register_new_user_successfully -> Register New User Successfully
    if method_part.startswith("test_"):
        method_part = method_part[5:]  # Remove "test_"
    test_name = " ".join(word.capitalize() for word in method_part.split("_"))

    return classname, test_name


def transform_junit_xml(input_path, output_path):
    """Transform Robot Framework JUnit XML to pytest-compatible format."""
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Transform all testcase elements in-place (keep nested structure)
    for testcase in root.findall('.//testcase'):
        classname = testcase.get('classname', '')
        name = testcase.get('name', '')

        if classname and name:
            # Convert to pytest format: tests.robot.api.auth::test_method
            pytest_name = to_pytest_format(classname, name)
            parts = pytest_name.split("::")
            if len(parts) == 2:
                # Set classname to module path and name to test method
                testcase.set('classname', parts[0])  # tests.robot.api.auth
                testcase.set('name', parts[1])       # test_access_protected_endpoint_...

    # Write transformed XML (keeps nested structure)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    print(f"Transformed JUnit XML written to {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: transform_robot_junit.py <input.xml> <output.xml>", file=sys.stderr)
        sys.exit(1)

    input_xml = sys.argv[1]
    output_xml = sys.argv[2]
    transform_junit_xml(input_xml, output_xml)
