# -*- coding: UTF-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (LogoutView,
                    ChangePasswordView,

                    ConfirmPasswordChangeRequest,
                    ConfirmEmailChangeRequest,

                    ConfirmEmailValidationRequest,
                    SendEmailValidationRequest,

                    AccountSettingsView,)


urlpatterns = patterns('',
    url(r'^email_not_validated/$', login_required(TemplateView.as_view(template_name='me/email-validation-pending.html')), name='email-not-validated'),
    url(r'^email_not_validated/send/$', login_required(SendEmailValidationRequest.as_view()), name='send-email-validation-request'),
    url(r'^email_confirmed/(?P<token>.*)/$', ConfirmEmailValidationRequest.as_view(), name='confirm-email-address'),

    url(r'^email_change_confirmed/(?P<token>.*)/$', ConfirmEmailChangeRequest.as_view(), name='confirm-email-change'),
    url(r'^password_change_confirmed/(?P<token>.*)/$', ConfirmPasswordChangeRequest.as_view(), name='confirm-password-change'),

    #url(r'^settings/confirm/$', login_required(ConfirmAccountView.as_view()), name='confirm-account'),
    url(r'^settings/change-password/$', login_required(ChangePasswordView.as_view()), name='change-password'),

    url(r'^settings/$', login_required(AccountSettingsView.as_view()), name='settings'),
    url(r'^logout/$', login_required(LogoutView.as_view()), name='logout'),
)
