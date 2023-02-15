#!/usr/bin/env python3
"""
Tests cert_easy

Copyright 2017-2023 Nicolas BEGUIER
Licensed under the Apache License
Written by Nicolas BEGUIER (nicolas_beguier@hotmail.com)
"""

# Standard library imports
import os
import sys

# Own library
MYPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, MYPATH + '/../')
import Android_Activity_Swagger as aas

# Debug
from pdb import set_trace as st

WRONG_ACTIVITY_SWAGGER = {
    'Boolean': [
        'open_from_notification',
        'open_from_reminder_notification',
        'open_from_abandonned_cart_notification',
        'from_deeplink'
    ],
    'Int': ['intent_request_code'],
    'data-uri': True}

TRUENAME_ACTIVITY_SWAGGER = {
    'Boolean': [
        'open_from_notification',
        'open_from_reminder_notification',
        'open_from_abandonned_cart_notification',
        'from_deeplink'],
    'Int': ['intent_request_code', 'source', 'PictureGalleryKt.POSITION_KEY'],
    'data-uri': True,
    'String': ['ad_id', 'requestId'],
    'Parcelable': ['ad_referrer', 'SearchResultsFragment.SEARCH_REQUEST_MODEL_KEY']}

LAUNCHER_ACTIVITY_SWAGGER = {
    "Boolean": [
        "open_from_notification",
        "open_from_reminder_notification",
        "open_from_abandonned_cart_notification",
        "from_deeplink"
    ],
    "Int": [
        "intent_request_code",
        "source",
        "PictureGalleryKt.POSITION_KEY"
    ],
    "Parcelable": [
        "ad_referrer",
        "SearchResultsFragment.SEARCH_REQUEST_MODEL_KEY"
    ],
    "String": [
        "ad_id",
        "requestId"
    ],
    "data-uri": True
}

ROUTING_ACTIVITY_SWAGGER = {
    "Int": [
        "source",
        "PictureGalleryKt.POSITION_KEY"
    ],
    "Parcelable": [
        "ad_referrer",
        "SearchResultsFragment.SEARCH_REQUEST_MODEL_KEY"
    ],
    "String": [
        "ad_id",
        "requestId"
    ]
}

def test_read_manifest(capsys):
    aas.read_manifest('tests/AndroidManifest.xml')
    out, err = capsys.readouterr()
    assert out == 'Package: com.example\n\ncom.example.activity.MyLauncherActivity\ncom.example.activity.WrongName\ncom.example.ui.RoutingActivity\n'
    assert err == ''

def test_activity_params_wrong_err(capsys):
    aas.get_activity_params('com.example.activity.WrongName', {'_result': {}, '_parsing': {}}, '.')
    out, err = capsys.readouterr()
    assert out == './com/example/activity/WrongName.java doesn\'t exist !\n'
    assert err == ''

def test_activity_params_wrong_ok(capsys):
    swagger = {'_result': {}, '_parsing': {}}
    aas.get_activity_params('com.example.activity.WrongName', swagger, 'tests/')
    _, err = capsys.readouterr()
    assert swagger['_result'] == WRONG_ACTIVITY_SWAGGER
    assert err == ''

def test_activity_params_true_ok(capsys):
    swagger = {'_result': {}, '_parsing': {}}
    aas.get_activity_params('com.example.activity.WrongName$TrueName', swagger, 'tests/')
    _, err = capsys.readouterr()
    assert swagger['_result'] == TRUENAME_ACTIVITY_SWAGGER
    assert err == ''

def test_activity_params_launcher_ok(capsys):
    swagger = {'_result': {}, '_parsing': {}}
    aas.get_activity_params('com.example.activity.MyLauncherActivity', swagger, 'tests/')
    _, err = capsys.readouterr()
    assert swagger['_result'] == LAUNCHER_ACTIVITY_SWAGGER
    assert err == ''

def test_activity_params_launcher_ok(capsys):
    swagger = {'_result': {}, '_parsing': {}}
    aas.get_activity_params('com.example.activity.MyLauncherActivity', swagger, 'tests/')
    _, err = capsys.readouterr()
    assert swagger['_result'] == LAUNCHER_ACTIVITY_SWAGGER
    assert err == ''

def test_activity_params_routing_ok(capsys):
    swagger = {'_result': {}, '_parsing': {}}
    aas.get_activity_params('com.example.ui.RoutingActivity', swagger, 'tests/')
    _, err = capsys.readouterr()
    assert swagger['_result'] == ROUTING_ACTIVITY_SWAGGER
    assert err == ''

def test_adb_helper(capsys):
    aas.print_adb_helper(ROUTING_ACTIVITY_SWAGGER, 'com.example', 'com.example.ui.RoutingActivity')
    out, err = capsys.readouterr()
    assert out == 'adb shell am start -n com.example.ui.RoutingActivity/com.example --ei source 0\nadb shell am start -n com.example.ui.RoutingActivity/com.example --ei PictureGalleryKt.POSITION_KEY 0\nadb shell am start -n com.example.ui.RoutingActivity/com.example --es ad_id "some_string"\nadb shell am start -n com.example.ui.RoutingActivity/com.example --es requestId "some_string"\n'
    assert err == ''
