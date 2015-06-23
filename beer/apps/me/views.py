# -*- coding: utf-8 -*-
from django.http import Http404
from django.core import signing
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, UpdateView, RedirectView
from django.views.generic.edit import BaseUpdateView
from django.shortcuts import get_object_or_404

from beer.mixins import (AjaxFormView, LogOutMixin)

from .mailers import ValidateEmailMailer

from .forms import (ChangePasswordForm,
                    AccountSettingsForm,)

import json
import logging
logger = logging.getLogger('django.request')


User = get_user_model()


class LogoutView(LogOutMixin, RedirectView):
    url = '/'


class SendEmailValidationRequest(BaseUpdateView):
    def post(self, request, *args, **kwargs):
        """
        Jsut send it; if the user has already validated then we will catch that
        on the confirmation view
        """
        mailer = ValidateEmailMailer(((request.user.get_full_name(), request.user.email,),))
        mailer.process(user=request.user)

        content = {
            'detail': 'Email sent'
        }
        return HttpResponse(json.dumps(content), content_type='application/json', **kwargs)


# ------------------------------------------
# Start Settings Change Confirmation Views
# ------------------------------------------


class BaseConfirmValidationRequest(RedirectView):
    url = '/'  # redirect to home

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        self.user = self.get_user(token=kwargs.get('token'))
        self.profile = self.user.profile

        self.save()
        return super(BaseConfirmValidationRequest, self).dispatch(request=request, *args, **kwargs)

    def get_user(self, token):
        try:
            pk = signing.loads(token, salt=settings.URL_ENCODE_SECRET_KEY)
        except signing.BadSignature:
            raise Http404
        return get_object_or_404(get_user_model(), pk=pk)

    def save(self):
        raise NotImplementedError


class ConfirmEmailValidationRequest(BaseConfirmValidationRequest):

    def save(self):
        self.profile.validated_email = True
        self.profile.save(update_fields=['data'])

        messages.success(self.request, 'Thanks. You have confirmed your email address.')
        logger.info(u'User: %s has validated their email' % self.user)


class ConfirmEmailChangeRequest(BaseConfirmValidationRequest):
    """
    When a user confirms that they want to change their email they come
    here and it does that for them.
    """

    def save(self):
        email = self.profile.data.get('validation_required_temp_email', False)
        original_email = self.user.email

        if email and email is not False:
            self.user.email = email
            self.user.save(update_fields=['email'])

            # remove temp password
            del self.profile.data['validation_required_temp_email']
            # set validated_email to True
            self.profile.validated_email = True
            self.profile.save(update_fields=['data'])

        messages.success(self.request, 'Congratulations. Your email has been changed. Please login with your new email.')
        logger.info(u'User: %s has confirmed their change of email address from: %s to: %s' % (self.user, original_email, self.user.email))


class ConfirmPasswordChangeRequest(BaseConfirmValidationRequest):
    """
    When a user confirms that they want to change their password they come
    here and it does that for them.
    """

    def save(self):
        password = self.profile.data.get('validation_required_temp_password', False)

        if password and password is not False:
            self.user.password = password
            self.user.save(update_fields=['password'])
            # remove temp password
            del self.profile.data['validation_required_temp_password']
            self.profile.save(update_fields=['data'])

        messages.success(self.request, 'Congratulations. Your password has been changed. Please login with your new password.')
        logger.info(u'User: %s has confirmed their change of password' % self.user)

# ----------------------------
# End Confirmation Views
# ----------------------------


class AccountSettingsView(UpdateView):
    form_class = AccountSettingsForm
    model = User
    success_url = reverse_lazy('me:settings')
    template_name = 'me/settings/account.html'

    def get_form_kwargs(self):
        kwargs = super(AccountSettingsView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def password_form(self):
        return ChangePasswordForm(request=self.request,
                                  user=self.request.user)


class ChangePasswordView(AjaxFormView, FormView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('me:settings')
    template_name = 'me/settings/change-password.html'

    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'user': self.request.user
        })
        return kwargs
