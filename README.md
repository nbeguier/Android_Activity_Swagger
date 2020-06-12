# Android_Activity_Swagger

Give the Swagger (or hints) of Android Activities from apk


## Example

```bash
$ cd tests/
$ ../Android_Activity_Swagger.py com.example.activity.WrongName
Found activity: com.example.activity.WrongName
Activity's file path: com/example/activity/WrongName.java
[com/example/activity/WrongName.java:+43] [onCreate]                 this.f4672b = getIntent().getExtras();
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
    ]
}
```

## Tests

cd tests/
Android_Activity_Swagger.py com.example.activity.WrongName
Android_Activity_Swagger.py 'com.example.activity.WrongName$TrueName'
Android_Activity_Swagger.py com.example.activity.MyLauncherActivity
Android_Activity_Swagger.py com.example.ui.RoutingActivity

# License
Android_Activity_Swagger is an open source and free software released under the [AGPL](https://github.com/nbeguier/Android_Activity_Swagger/blob/master/LICENSE) (Affero General Public License). We are committed to ensure that Android_Activity_Swagger will remain a free and open source project on the long-run.

# Copyright
Copyright (C) 2020  Nicolas Beguier; ([nbeguier](https://beguier.eu/nicolas/) - nicolas_beguier[at]hotmail[dot]com)
