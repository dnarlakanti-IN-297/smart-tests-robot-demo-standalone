#!/usr/bin/env python3
"""
Extract Robot Framework test names from JUnit XML.
This generates a list compatible with Smart Tests subset/recording.
"""
import sys
import xml.etree.ElementTree as ET

def extract_test_names(junit_xml_path):
    """Extract test names from JUnit XML file."""
    tree = ET.parse(junit_xml_path)
    root = tree.getroot()

    test_names = []
    for testcase in root.findall('.//testcase'):
        classname = testcase.get('classname', '')
        name = testcase.get('name', '')
        if classname and name:
            # Format: Robot.Api.Auth.Register New User Successfully
            full_name = f"{classname}.{name}"
            test_names.append(full_name)

    return test_names

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_robot_tests.py <junit.xml>", file=sys.stderr)
        sys.exit(1)

    junit_xml = sys.argv[1]
    test_names = extract_test_names(junit_xml)

    for test in test_names:
        print(test)
