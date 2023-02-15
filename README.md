# Android_Activity_Swagger

Give the Swagger (or hints) of Android Activities from apk

## Prerequisites

You need a decompiled apk file, using jadx for instance:

```bash
$ ls base.apk
$ jadx base.apk -d decompiled_apk/
$ cd decompiled_apk/
```

## Usage

```bash
$ python Android_Activity_Swagger.py --help
usage: Android_Activity_Swagger.py [-h] [--version] [--package PACKAGE] [--adb] [--verbose] [--read-manifest] activity

positional arguments:
  activity              Activity

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --package PACKAGE, -p PACKAGE
                        Package.
  --adb, -a             ADB helper.
  --verbose, -v         Verbose output.
  --read-manifest, -r   Read AndroidManifest.xml and extract exported activities.
```

## Examples

```bash
# List all exported activities
$ python Android_Activity_Swagger.py -r tests/AndroidManifest.xml
Package: com.example

com.example.activity.MyLauncherActivity
com.example.activity.WrongName
com.example.ui.RoutingActivity
```

```bash
# Display com.example.activity.WrongName
$ cd tests/

$ python ../Android_Activity_Swagger.py com.example.activity.WrongName
[com/example/activity/WrongName.java:+43] [onCreate]                 this.f4672b = getIntent().getExtras();
[com/example/activity/WrongName.java:+53] [onCreate]             if (this.f4672b != null && this.f4672b.getBoolean("open_from_notification", false)) {
[com/example/activity/WrongName.java:+54] [onCreate]                 if (this.f4672b.getBoolean("open_from_reminder_notification", false)) {
[com/example/activity/WrongName.java:+56] [onCreate]                 } else if (this.f4672b.getBoolean("open_from_abandonned_cart_notification", false)) {
[com/example/activity/WrongName.java:+61] [onCreate]                 this.g = this.f4672b.getInt("intent_request_code", -1);
[com/example/activity/WrongName.java:+62] [onCreate]                 this.e = this.f4672b.getBoolean("from_deeplink");
[com/example/activity/WrongName.java:+77] [extractData]                 str = getIntent().getDataString();
{
    "Boolean": [
        "open_from_notification",
        "open_from_reminder_notification",
        "open_from_abandonned_cart_notification",
        "from_deeplink"
    ],
    "Int": [
        "intent_request_code"
    ],
    "data-uri": true
}
```

```bash
# Display com.example.activity.WrongName with verbosity
$ python ../Android_Activity_Swagger.py com.example.activity.WrongName --verbose
Found activity: com.example.activity.WrongName
Activity's file path: com/example/activity/WrongName.java
[com/example/activity/WrongName.java:+43] [onCreate]                 this.f4672b = getIntent().getExtras();
[com/example/activity/WrongName.java:+53] [onCreate]             if (this.f4672b != null && this.f4672b.getBoolean("open_from_notification", false)) {
[com/example/activity/WrongName.java:+54] [onCreate]                 if (this.f4672b.getBoolean("open_from_reminder_notification", false)) {
[com/example/activity/WrongName.java:+56] [onCreate]                 } else if (this.f4672b.getBoolean("open_from_abandonned_cart_notification", false)) {
[com/example/activity/WrongName.java:+61] [onCreate]                 this.g = this.f4672b.getInt("intent_request_code", -1);
[com/example/activity/WrongName.java:+62] [onCreate]                 this.e = this.f4672b.getBoolean("from_deeplink");
[com/example/activity/WrongName.java:+77] [extractData]                 str = getIntent().getDataString();
Found parent: Activity

{
    "Boolean": [
        "open_from_notification",
        "open_from_reminder_notification",
        "open_from_abandonned_cart_notification",
        "from_deeplink"
    ],
    "Int": [
        "intent_request_code"
    ],
    "data-uri": true
}
```

```bash
# Display com.example.activity.WrongName with some adb command example
$ python ../Android_Activity_Swagger.py com.example.activity.WrongName -p com.example --adb
[com/example/activity/WrongName.java:+43] [onCreate]                 this.f4672b = getIntent().getExtras();
[com/example/activity/WrongName.java:+53] [onCreate]             if (this.f4672b != null && this.f4672b.getBoolean("open_from_notification", false)) {
[com/example/activity/WrongName.java:+54] [onCreate]                 if (this.f4672b.getBoolean("open_from_reminder_notification", false)) {
[com/example/activity/WrongName.java:+56] [onCreate]                 } else if (this.f4672b.getBoolean("open_from_abandonned_cart_notification", false)) {
[com/example/activity/WrongName.java:+61] [onCreate]                 this.g = this.f4672b.getInt("intent_request_code", -1);
[com/example/activity/WrongName.java:+62] [onCreate]                 this.e = this.f4672b.getBoolean("from_deeplink");
[com/example/activity/WrongName.java:+77] [extractData]                 str = getIntent().getDataString();
{
    "Boolean": [
        "open_from_notification",
        "open_from_reminder_notification",
        "open_from_abandonned_cart_notification",
        "from_deeplink"
    ],
    "Int": [
        "intent_request_code"
    ],
    "data-uri": true
}
adb shell am start -n com.example/com.example.activity.WrongName --ez open_from_notification true
adb shell am start -n com.example/com.example.activity.WrongName --ez open_from_reminder_notification true
adb shell am start -n com.example/com.example.activity.WrongName --ez open_from_abandonned_cart_notification true
adb shell am start -n com.example/com.example.activity.WrongName --ez from_deeplink true
adb shell am start -n com.example/com.example.activity.WrongName --ei intent_request_code 0
adb shell am start -n com.example/com.example.activity.WrongName -d https://github.com/nbeguier/
```

## Tests

```bash
cd tests/
../Android_Activity_Swagger.py com.example.activity.WrongName
../Android_Activity_Swagger.py 'com.example.activity.WrongName$TrueName'
../Android_Activity_Swagger.py com.example.activity.MyLauncherActivity
../Android_Activity_Swagger.py com.example.ui.RoutingActivity
../Android_Activity_Swagger.py com.example.ui.RoutingActivity -p com.example --adb
```

## License
Android_Activity_Swagger is an open source and free software released under the [AGPL](https://github.com/nbeguier/Android_Activity_Swagger/blob/master/LICENSE) (Affero General Public License). We are committed to ensure that Android_Activity_Swagger will remain a free and open source project on the long-run.

## Copyright
Copyright (C) 2020-2023  Nicolas Beguier; ([nbeguier](https://beguier.eu/nicolas/) - nicolas_beguier[at]hotmail[dot]com)
