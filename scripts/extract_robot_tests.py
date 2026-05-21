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
    Convert Robot Framework test to pytest file path format.

    Input:
      classname: "Robot.Integration.Issue Lifecycle"
      test_name: "Bug Fix Workflow With Type And Priority"

    Output:
      "tests/robot/integration/issue_lifecycle.py::test_bug_fix_workflow_with_type_and_priority"
    """
    # Remove "Robot." prefix
    if classname.startswith("Robot."):
        suite_path = classname[6:]  # Remove "Robot."
    else:
        suite_path = classname

    # Convert suite path to file path: "Integration.Issue Lifecycle" -> "tests/robot/integration/issue_lifecycle.py"
    # Use forward slashes for file paths, convert to lowercase, replace spaces with underscores
    # Use .py extension for pytest compatibility (Smart Tests expects .py files)
    suite_parts = suite_path.split(".")
    file_parts = [re.sub(r'\s+', '_', part.lower()) for part in suite_parts]
    file_path = "tests/robot/" + "/".join(file_parts) + ".py"

    # Convert test name to method format
    method_name = "test_" + re.sub(r'[^a-zA-Z0-9]+', '_', test_name).lower().strip('_')

    # Use raw profile format: file=path#testCase=name
    return f"file={file_path}#testCase={method_name}"


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
