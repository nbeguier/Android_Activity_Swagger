#!/usr/bin/env python
"""
Android Activity Swagger

Copyright (C) 2020-2021  Nicolas Beguier

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
from argparse import ArgumentParser
import json
import os
import re

# Debug
# from pdb import set_trace as st

VERSION = '1.2.0'

def update_class(current_class, line):
    """
    Updates the current class if a new is found in line
    """
    match = re.search("(public|private) [a-zA-Z\ ]+ ([a-zA-Z]+)\(", line)
    if match:
        return match.group(2)
    return current_class

def print_extras(context, key=None):
    """
    Display found extra
    """
    color_line = re.sub("(get|has)[a-zA-Z]*Extras?", lambda m: "\x1b[38;5;75m{}\x1b[0m".format(m.group()), context['line'][:-1])
    if key is not None:
        color_line = re.sub(key, lambda m: "\x1b[38;5;76m{}\x1b[0m".format(m.group()), color_line)
    print("[{}:+{}] [{}] {}".format(context['activity_file_path'], context['line_n'], context['current_class'], color_line))
    return True

def print_data(context):
    """
    Display found data
    """
    if re.search("\.getData[a-zA-Z]*\(", context['line']):
        color_line = re.sub("getData[a-zA-Z]*", lambda m: "\x1b[38;5;76m{}\x1b[0m".format(m.group()), context['line'][:-1])
        print("[{}:+{}] [{}] {}".format(context['activity_file_path'], context['line_n'], context['current_class'], color_line))
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

def update_swagger(context, swagger):
    """
    Updates the swagger
    """
    added = False

    if context['current_class'] in swagger['_parsing']:
        for var in swagger['_parsing'][context['current_class']]:
            type_match = re.search("{}\.get([a-zA-Z]+)\(".format(var), context['line'])
            if type_match:
                key_type = type_match.group(1)
                key_name = '_unknown'
                key_match = re.search("{}\.get[a-zA-Z]+\(\"?([a-zA-Z\_\.]+)\"?".format(var), context['line'])
                if key_match:
                    key_name = key_match.group(1)
                if key_type not in swagger['_result']:
                    swagger['_result'][key_type] = list()
                if key_name not in swagger['_result'][key_type]:
                    swagger['_result'][key_type].append(key_name)
                print_extras(context, key=key_name)
                added = True

    # X = y.getExtras()
    getextras_match = re.search("([a-zA-Z\.]+) = [a-zA-Z\.\(\)]+\.getExtras\(\)", context['line'])
    if getextras_match:
        var = getextras_match.group(1)
        if context['current_class'] not in swagger['_parsing']:
            swagger['_parsing'][context['current_class']] = dict()
        if var not in swagger['_parsing'][context['current_class']]:
            swagger['_parsing'][context['current_class']][var] = ''

    # .getXExtra("Y"
    getextra_match = re.search("\.get([a-zA-Z]+)Extra\(", context['line'])
    if getextra_match:
        key_type = getextra_match.group(1)
        key_name = '_unknown'
        key_match = re.search("\.get[a-zA-Z]+\(\"?([a-zA-Z\_\.]+)\"?", context['line'])
        if key_match:
            key_name = key_match.group(1)
        if key_type not in swagger['_result']:
            swagger['_result'][key_type] = list()
        if key_name not in swagger['_result'][key_type]:
            swagger['_result'][key_type].append(key_name)
        print_extras(context, key=key_name)
        added = True

    if not added and re.search("\.(get|has)[a-zA-Z]*Extras?\(", context['line']):
        print_extras(context)

    return swagger

def get_activity_params(activity, swagger, is_recursive=False, verbosity=False):
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

    if verbosity:
        print("Found activity: {}".format(activity))
        print("Activity's file path: {}".format(activity_file_path))

    parent_name = None

    with open(activity_file_path, "r") as activity_file:
        line_n = 1
        current_class = None
        for line in activity_file.readlines():
            current_class = update_class(current_class, line)
            context = {
                'activity_file_path': activity_file_path,
                'current_class': current_class,
                'line': line,
                'line_n': line_n,
            }
            if print_data(context):
                swagger['_result']['data-uri'] = True
            swagger = update_swagger(context, swagger)
            parent_name = update_parent(parent_name, line, activity_name)
            line_n += 1

    if parent_name:
        if verbosity:
            print("Found parent: {}".format(parent_name))
            print("")
        parent = None
        with open(activity_file_path, "r") as activity_file:
            for line in activity_file.readlines():
                if ".{};".format(parent_name) in line and line.startswith("import"):
                    parent = line.split()[1].split(";")[0]
        if parent:
            get_activity_params(parent, swagger, is_recursive=True, verbosity=verbosity)

def print_adb_helper(swagger, activity, package):
    """
    [-a <ACTION>] [-d <DATA_URI>] [-t <MIME_TYPE>]
    [-c <CATEGORY> [-c <CATEGORY>] ...]
    [-e|--es <EXTRA_KEY> <EXTRA_STRING_VALUE> ...]
    [--esn <EXTRA_KEY> ...]
    [--ez <EXTRA_KEY> <EXTRA_BOOLEAN_VALUE> ...]
    [--ei <EXTRA_KEY> <EXTRA_INT_VALUE> ...]
    [--el <EXTRA_KEY> <EXTRA_LONG_VALUE> ...]
    [--ef <EXTRA_KEY> <EXTRA_FLOAT_VALUE> ...]
    [--eu <EXTRA_KEY> <EXTRA_URI_VALUE> ...]
    [--ecn <EXTRA_KEY> <EXTRA_COMPONENT_NAME_VALUE>]
    [--eia <EXTRA_KEY> <EXTRA_INT_VALUE>[,<EXTRA_INT_VALUE...]]
    [--ela <EXTRA_KEY> <EXTRA_LONG_VALUE>[,<EXTRA_LONG_VALUE...]]
    [--efa <EXTRA_KEY> <EXTRA_FLOAT_VALUE>[,<EXTRA_FLOAT_VALUE...]]
    [-n <COMPONENT>] [-f <FLAGS>]
    [--grant-read-uri-permission] [--grant-write-uri-permission]
    [--debug-log-resolution] [--exclude-stopped-packages]
    [--include-stopped-packages]
    [--activity-brought-to-front] [--activity-clear-top]
    [--activity-clear-when-task-reset] [--activity-exclude-from-recents]
    [--activity-launched-from-history] [--activity-multiple-task]
    [--activity-no-animation] [--activity-no-history]
    [--activity-no-user-action] [--activity-previous-is-top]
    [--activity-reorder-to-front] [--activity-reset-task-if-needed]
    [--activity-single-top] [--activity-clear-task]
    [--activity-task-on-home]
    [--receiver-registered-only] [--receiver-replace-pending]
    [--selector]
    [<URI> | <PACKAGE> | <COMPONENT>]
    """
    adb_args_map = {
        'String': '--es',
        'Boolean': '--ez',
        'Int': '--ei',
        'Long': '--el',
        'Float': '--ef',
        'data-uri': '-d',
    }
    adb_default_value_map = {
        'String': '"some_string"',
        'Boolean': 'true',
        'Int': '0',
        'Long': '0',
        'Float': '0',
        'data-uri': 'https://github.com/nbeguier/',
    }
    for extra_type in swagger:
        # Ignore extra types
        if extra_type in ['Parcelable']:
            continue
        # Data-uri type
        if extra_type == 'data-uri':
            print(f'adb shell am start -n {package}/{activity} ' + \
                f'{adb_args_map[extra_type]} {adb_default_value_map[extra_type]}')
        else:
            for extra_key in swagger[extra_type]:
                print(f'adb shell am start -n {package}/{activity} ' + \
                    f'{adb_args_map[extra_type]} {extra_key} {adb_default_value_map[extra_type]}')

def main():
    """
    Main function
    """
    parser = ArgumentParser()

    parser.add_argument('--version', action='version', version=VERSION)

    parser.add_argument(
        'activity',
        action='store',
        help='Activity')
    parser.add_argument("--package", "-p", action="store",
                                help="Package.")
    parser.add_argument("--adb", "-a", action="store_true",
                        default=False, help="ADB helper.")
    parser.add_argument("--verbose", "-v", action="store_true",
                        default=False, help="Verbose output.")
    args = parser.parse_args()
    swagger = {'_result': dict(), '_parsing': dict()}
    get_activity_params(args.activity, swagger, verbosity=args.verbose)
    print(json.dumps(swagger['_result'], sort_keys=True, indent=4, separators=(',', ': ')))
    if args.adb:
        if not args.package:
            print('You should define the package to view ADB helper')
        else:
            print_adb_helper(swagger['_result'], args.activity, args.package)

if __name__ == '__main__':
    main()
