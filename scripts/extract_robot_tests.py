#!/usr/bin/env python3
"""
Extract Robot Framework test names from JUnit XML in pytest format.
This generates a list compatible with Smart Tests subset/recording.
"""
import sys
import xml.etree.ElementTree as ET
import re


def to_pytest_format(classname, test_name):
    """
    Convert Robot Framework test to pytest format.

    Input:
      classname: "Robot.Api.Auth"
      test_name: "Register New User Successfully"

    Output:
      "tests.robot.api.auth::test_register_new_user_successfully"
    """
    # Remove "Robot." prefix and convert to lowercase path
    if classname.startswith("Robot."):
        suite_path = classname[6:]  # Remove "Robot."
    else:
        suite_path = classname

    # Convert to pytest path: Api.Auth -> tests.robot.api.auth
    file_path = "tests.robot." + suite_path.lower().replace(".", ".")

    # Convert test name to pytest format
    method_name = "test_" + re.sub(r'[^a-zA-Z0-9]+', '_', test_name).lower().strip('_')

    return f"{file_path}::{method_name}"


def extract_test_names(junit_xml_path):
    """Extract test names from JUnit XML file in pytest format."""
    tree = ET.parse(junit_xml_path)
    root = tree.getroot()

    test_names = []
    for testcase in root.findall('.//testcase'):
        classname = testcase.get('classname', '')
        name = testcase.get('name', '')
        if classname and name:
            # Convert to pytest format for Smart Tests compatibility
            pytest_name = to_pytest_format(classname, name)
            test_names.append(pytest_name)

    return test_names


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_robot_tests.py <junit.xml>", file=sys.stderr)
        sys.exit(1)

    junit_xml = sys.argv[1]
    test_names = extract_test_names(junit_xml)

    for test in test_names:
        print(test)
