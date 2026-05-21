#!/usr/bin/env python3
"""
Extract Robot Framework test names from JUnit XML.
This generates a list compatible with Smart Tests subset/recording.
"""
import sys
import xml.etree.ElementTree as ET

def extract_test_names(junit_xml_path, output_format='robot'):
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

            if output_format == 'raw':
                # Convert to Smart Tests raw format
                # Robot.Api.Auth.Register New User Successfully
                # -> file=Robot.Api.Auth#test=Register New User Successfully
                test_names.append(f"file={classname}#test={name}")
            else:
                # Keep original Robot format
                test_names.append(full_name)

    return test_names

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: extract_robot_tests.py <junit.xml> [format]", file=sys.stderr)
        print("  format: 'robot' (default) or 'raw' (for Smart Tests raw profile)", file=sys.stderr)
        sys.exit(1)

    junit_xml = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'robot'
    test_names = extract_test_names(junit_xml, output_format)

    for test in test_names:
        print(test)
