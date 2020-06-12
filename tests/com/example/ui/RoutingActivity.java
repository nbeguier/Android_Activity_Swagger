package com.example.ui.RoutingActivity;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.MenuItem;
import android.view.View;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

public final class RoutingActivity extends AppCompatActivity {

    public void onCreate(@Nullable Bundle bundle) {
        AndroidInjection.inject((Activity) this);
        super.onCreate(bundle);
        if (getIntent() == null) {
            finish();
            return;
        }
        setContentView((int) R.layout.activity_display_ads);
        Intent intent = getIntent();
        Intrinsics.checkExpressionValueIsNotNull(intent, "intent");
        extractArguments(intent);
        if (!isSetupAlreadyDone()) {
            if (isSingleAdDisplay()) {
                fetchSingleAdThenDisplayAdView();
            } else {
                displayAdView();
            }
        }
    }

    /* access modifiers changed from: protected */
    public void onResume() {
        super.onResume();
    }

    /* access modifiers changed from: protected */
    public void onPause() {
        super.onPause();
    }

    /* access modifiers changed from: protected */
    public void onStop() {
        super.onStop();
    }

    public void finish() {
        Intent intent = new Intent();
        intent.putExtra("ad_position", this.currentPosition);
        setResult(-1, intent);
        super.finish();
    }

    private final boolean isSingleAdDisplay() {
        return this.adId != null;
    }

    private final void extractArguments(Intent intent) {
        int intExtra = intent.getIntExtra("source", -1);
        this.source = intExtra;
        if (intExtra != -1) {
            this.adId = intent.getStringExtra("ad_id");
            this.adReferrerInfo = (AdReferrerInfo) intent.getParcelableExtra("ad_referrer");
            this.currentPosition = intent.getIntExtra(PictureGalleryKt.POSITION_KEY, 0);
            this.searchRequestModel = (SearchRequestModel) intent.getParcelableExtra(SearchResultsFragment.SEARCH_REQUEST_MODEL_KEY);
            this.requestId = intent.getStringExtra("requestId");
            return;
        }
        throw new IllegalArgumentException(("The source hasn't been set into the intent !\n Intent : " + intent + " \n Extras " + intent.getExtras()).toString());
    }

}
