package com.example.activity;

import android.app.Activity;
import android.app.AlarmManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.res.Configuration;
import android.net.Uri;
import android.os.Bundle;
import android.support.v4.app.NotificationCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v4.util.Pair;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.app.AppCompatDelegate;
import android.support.v7.widget.Toolbar;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.Toast;
import com.example.ui.RoutingActivity;


public class WrongName extends Activity {


    public static class TrueName extends RoutingActivity {


        public void onCreate(Bundle bundle) {
            super.onCreate(bundle);
            E();
            AppCompatDelegate.setCompatVectorFromResourcesEnabled(true);
            setContentView(j());
            this.j = ButterKnife.a((Activity) this);
            t();
            u();
            if (getIntent() != null) {
                this.f4672b = getIntent().getExtras();
            } else {
                this.f4672b = new Bundle();
            }
            ac.a(getClass().getSimpleName(), extractData());
            new z().a((Activity) this, getClass().getSimpleName());
            extractData();
            if (App.f4659b.h() == null) {
                App.f4659b.a(new e(this));
            }
            if (this.f4672b != null && this.f4672b.getBoolean("open_from_notification", false)) {
                if (this.f4672b.getBoolean("open_from_reminder_notification", false)) {
                    ac.a(ac.b.OPEN_NOTIFICATION.toString(), ac.a.OPEN_FROM_REMINDER.toString(), "", 1);
                } else if (this.f4672b.getBoolean("open_from_abandonned_cart_notification", false)) {
                    ac.a(ac.b.OPEN_NOTIFICATION.toString(), ac.a.OPEN_FROM_ABANDONNED_CART.toString(), "", 1);
                }
            }
            if (this.f4672b != null) {
                this.g = this.f4672b.getInt("intent_request_code", -1);
                this.e = this.f4672b.getBoolean("from_deeplink");
            }
            w();
            v();
            y();
            A();
            B();
            D();
        }

        public void extractData(String str) {
            int i2;
            int i3;
            int i4;
            if (Utils.isStringEmpty(str)) {
                str = getIntent().getDataString();
            }
            if (TextUtils.isEmpty(str)) {
                return;
            }
            if (str.contains("home")) {
                if (this instanceof MainActivity) {
                    finish();
                }
                DeeplinkUtils.launchHomeFromDeeplink(this);
            } else if (str.startsWith("example://catalog")) {
                Map<String, Object> splitQueryUrl = Utils.splitQueryUrl(str);
                try {
                    i2 = Integer.parseInt((String) splitQueryUrl.get("id_category"));
                } catch (Exception e2) {
                    AppUtilsKt.printExceptionStacktrace(e2);
                    i2 = -1;
                }
                try {
                    i3 = Integer.parseInt((String) splitQueryUrl.get("id_selection"));
                } catch (Exception e3) {
                    AppUtilsKt.printExceptionStacktrace(e3);
                    i3 = -1;
                }
                try {
                    i4 = Integer.parseInt((String) splitQueryUrl.get("brand_id"));
                } catch (Exception e4) {
                    AppUtilsKt.printExceptionStacktrace(e4);
                    i4 = -1;
                }
                if (i4 > 0) {
                    DeeplinkUtils.launchCatalogFromDeeplink(this, 0, 0, i4);
                } else if (i2 < 0 && i3 < 0) {
                    DeeplinkUtils.launchHomeFromDeeplink(this);
                } else if (i2 > 0 && i3 > 0) {
                    a(i2, i3, (String) null);
                } else if (i2 > 0) {
                    Category c2 = ao.c(i2);
                    if (c2 == null) {
                        DeeplinkUtils.launchHomeFromDeeplink(this);
                    } else {
                        DeeplinkUtils.launchCategoryFromDeeplink(c2);
                    }
                } else if (i3 > 0) {
                    a(0, i3, (String) null);
                }
            } else if (str.startsWith("example://sell") || str.startsWith("example://wishlist") || str.startsWith("example://product") || str.startsWith("example://cart")) {
                try {
                    Intent intent = new Intent();
                    intent.setData(Uri.parse(str));
                    startActivity(intent);
                } catch (Throwable th) {
                    AppUtilsKt.printExceptionStacktrace(th);
                }
            }
        }
    }
}
