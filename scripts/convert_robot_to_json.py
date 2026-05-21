#!/usr/bin/env python3
"""
Convert Robot Framework JUnit XML to Smart Tests raw JSON format.
This bypasses the pytest profile limitations.
"""
import json
import xml.etree.ElementTree as ET
import sys
import re


def to_test_path(classname, test_name):
    """
    Convert Robot Framework test to raw format testPath.

    Input:
      classname: "Robot.Api.Auth"
      test_name: "Register New User Successfully"

    Output:
      "file=tests/robot/api/auth.py#testCase=test_register_new_user_successfully"
    """
    # Remove "Robot." prefix
    if classname.startswith("Robot."):
        suite_path = classname[6:]
    else:
        suite_path = classname

    # Convert to file path
    suite_parts = suite_path.split(".")
    file_parts = [re.sub(r'\s+', '_', part.lower()) for part in suite_parts]
    file_path = "tests/robot/" + "/".join(file_parts) + ".py"

    # Convert test name to method format
    method_name = "test_" + re.sub(r'[^a-zA-Z0-9]+', '_', test_name).lower().strip('_')

    # Raw format: file=path#testCase=name
    return f"file={file_path}#testCase={method_name}"


def convert_junit_to_json(junit_path, json_path):
    """Convert Robot Framework JUnit XML to Smart Tests JSON format."""
    tree = ET.parse(junit_path)
    root = tree.getroot()

    test_cases = []
    for testcase in root.findall('.//testcase'):
        classname = testcase.get('classname', '')
        name = testcase.get('name', '')
        time = float(testcase.get('time', '0'))

        if not classname or not name:
            continue

        test_path = to_test_path(classname, name)

        # Determine status from child elements
        if testcase.find('failure') is not None:
            status = "TEST_FAILED"
        elif testcase.find('error') is not None:
            status = "TEST_FAILED"
        elif testcase.find('skipped') is not None:
            status = "TEST_SKIPPED"
        else:
            status = "TEST_PASSED"

        test_case = {
            "testPath": test_path,
            "duration": time,
            "status": status
        }
        test_cases.append(test_case)

    output = {"testCases": test_cases}

    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Converted {len(test_cases)} tests to JSON format")
    print(f"JSON written to {json_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: convert_robot_to_json.py <input.xml> <output.json>", file=sys.stderr)
        sys.exit(1)

    junit_xml = sys.argv[1]
    output_json = sys.argv[2]
    convert_junit_to_json(junit_xml, output_json)
