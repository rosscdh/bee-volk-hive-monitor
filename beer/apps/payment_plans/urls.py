# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import (PaymentListView,
                    PlanListView,
                    PlanChangeView,
                    AccountCancelView,
                    WelcomeView,

                    TwoFactorDisableView,
                    TwoFactorEnableView,
                    TwoFactorVerifyView,

                    AccountSettingsView,)


urlpatterns = patterns(
    '',
    url(r'^welcome/$', login_required(WelcomeView.as_view()), name='welcome'),
    url(r'^payments/$', login_required(PaymentListView.as_view()), name='payment-list'),
    url(r'^plans/(?P<plan>[a-z0-9_-]{1,25})/$', login_required(PlanChangeView.as_view()), name='plan-change'),
    url(r'^plans/$', login_required(PlanListView.as_view()), name='plan-list'),

    url(r'^settings/two-factor/disable/$', login_required(TwoFactorDisableView.as_view()), name='two-factor-disable'),
    url(r'^settings/two-factor/enable/$', login_required(TwoFactorEnableView.as_view()), name='two-factor-enable'),
    url(r'^settings/two-factor/verify/$', login_required(TwoFactorVerifyView.as_view()), name='two-factor-verify'),
    url(r'^settings/$', login_required(AccountSettingsView.as_view()), name='settings'),

    url(r'^cancel/$', login_required(AccountCancelView.as_view()), name='cancel'),
)
