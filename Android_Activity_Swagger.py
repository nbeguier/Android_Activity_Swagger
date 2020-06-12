#!/usr/bin/env python
"""
Android Activity Swagger

Copyright (C) 2020  Nicolas Beguier

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import json
import os
import re
import sys

# Debug
# from pdb import set_trace as st

VERSION = '1.0.0'

ACTIVITY = sys.argv[1]

def update_class(current_class, line):
    """
    Updates the current class if a new is found in line
    """
    match = re.search("(public|private) [a-zA-Z\ ]+ ([a-zA-Z]+)\(", line)
    if match:
        return match.group(2)
    return current_class

def print_extras(line, line_n, activity_file_path, current_class):
    """
    Display found extra
    """
    if re.search("\.(get|has)[a-zA-Z]*Extras?\(", line):
        color_line = re.sub("(get|has)[a-zA-Z]*Extras?", lambda m: "\x1b[38;5;75m{}\x1b[0m".format(m.group()), line[:-1])
        print("[{}:+{}] [{}] {}".format(activity_file_path, line_n, current_class, color_line))
        return True
    return False

def print_data(line, line_n, activity_file_path, current_class):
    """
    Display found data
    """
    if re.search("\.getData[a-zA-Z]*\(", line):
        color_line = re.sub("getData[a-zA-Z]*", lambda m: "\x1b[38;5;76m{}\x1b[0m".format(m.group()), line[:-1])
        print("[{}:+{}] [{}] {}".format(activity_file_path, line_n, current_class, color_line))
        return True
    return False

def update_parent(value, line, activity_name):
    """
    Returns parent if exists
    """
    if value is not None:
        return value
    if "class {}".format(activity_name) in line and "extends" in line:
        return line.split("extends")[1].split()[0]
    return None

def update_swagger(swagger, line, current_class):
    """
    Updates the swagger
    """
    if current_class in swagger['_parsing']:
        for var in swagger['_parsing'][current_class]:
            type_match = re.search("{}\.get([a-zA-Z]+)\(".format(var), line)
            if type_match:
                key_type = type_match.group(1)
                key_name = '_unknown'
                key_match = re.search("{}\.get[a-zA-Z]+\(\"?([a-zA-Z\_\.]+)\"?".format(var), line)
                if key_match:
                    key_name = key_match.group(1)
                if key_type not in swagger['_result']:
                    swagger['_result'][key_type] = list()
                swagger['_result'][key_type].append(key_name)

    # X = y.getExtras()
    getextras_match = re.search("([a-zA-Z\.]+) = [a-zA-Z\.\(\)]+\.getExtras\(\)", line)
    if getextras_match:
        var = getextras_match.group(1)
        if current_class not in swagger['_parsing']:
            swagger['_parsing'][current_class] = dict()
        if var not in swagger['_parsing'][current_class]:
            swagger['_parsing'][current_class][var] = ''

    # .getXExtra("Y"
    getextra_match = re.search("\.get([a-zA-Z]+)Extra\(", line)
    if getextra_match:
        key_type = getextra_match.group(1)
        key_name = '_unknown'
        key_match = re.search("\.get[a-zA-Z]+\(\"?([a-zA-Z\_\.]+)\"?", line)
        if key_match:
            key_name = key_match.group(1)
        if key_type not in swagger['_result']:
            swagger['_result'][key_type] = list()
        swagger['_result'][key_type].append(key_name)

    return swagger

def get_activity_params(activity, swagger, is_recursive=False):
    """
    Returns the Activity parameters
    """
    activity_name = activity.split('.')[-1]
    # Activity name can be override by a '$'
    if '$' in activity_name:
        activity_name = activity_name.split('$')[1]
    activity_file_path = activity.replace(".", "/").split('$')[0] + ".java"

    if not os.path.exists(activity_file_path):
        if os.path.exists('sources/'+activity_file_path):
            activity_file_path = 'sources/'+activity_file_path
        else:
            if not is_recursive:
                print("{} doesn't exist !".format(activity_file_path))
            return

    print("Found activity: {}".format(activity))
    print("Activity's file path: {}".format(activity_file_path))

    parent_name = None

    with open(activity_file_path, "r") as activity_file:
        line_n = 1
        current_class = None
        for line in activity_file.readlines():
            current_class = update_class(current_class, line)
            print_extras(line, line_n, activity_file_path, current_class)
            print_data(line, line_n, activity_file_path, current_class)
            swagger = update_swagger(swagger, line, current_class)
            parent_name = update_parent(parent_name, line, activity_name)
            line_n += 1

    if parent_name:
        print("Found parent: {}".format(parent_name))
        print("")
        parent = None
        with open(activity_file_path, "r") as activity_file:
            for line in activity_file.readlines():
                if ".{};".format(parent_name) in line and line.startswith("import"):
                    parent = line.split()[1].split(";")[0]
        if parent:
            get_activity_params(parent, swagger, is_recursive=True)

def main():
    """
    Main function
    """
    swagger = {'_result': dict(), '_parsing': dict()}
    get_activity_params(ACTIVITY, swagger)
    print(json.dumps(swagger['_result'], sort_keys=True, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()
