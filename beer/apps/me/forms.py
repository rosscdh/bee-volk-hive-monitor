# -*- coding: utf-8 -*-
from django import forms
from django.contrib import messages
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.hashers import make_password

from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Field, Fieldset, HTML, Layout, Submit

from parsley.decorators import parsleyfy

from .mailers import (ValidatePasswordChangeMailer,
                      ValidateEmailChangeMailer)
from beer.mixins import ModalForm

import os
import logging
logger = logging.getLogger('django.request')


User = get_user_model()


class BaseAccountSettingsFields(forms.ModelForm):
    """
    Provides base field for various account settings forms
    """
    first_name = forms.CharField(
        error_messages={
            'required': "First name can't be blank."
        },
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'size': 15})
    )

    last_name = forms.CharField(
        error_messages={
            'required': "Last name can't be blank."
        },
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'size': 25})
    )

    email = forms.EmailField(
        error_messages={
            'invalid': "Email is invalid.",
            'required': "Email can't be blank."
        },
        help_text='Please Note: if you change your email, you will be logged out and an email will be sent to the current email address for confirmation. Your email will NOT be changed until you click on the link sent in the email.',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'size': 44})
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.attrs = {
            'parsley-validate': '',
        }
        self.helper.form_show_errors = False

        self.helper.layout = Layout(
            HTML('{% include "partials/form-errors.html" with form=form %}'),
            Fieldset(
                '',
                Div(
                    HTML('<label>Full name<span class="asteriskField">*</span></label>'),
                    Div(
                        Field('first_name', css_class='input-hg'),
                        Field('last_name', css_class='input-hg'),
                        css_class='form-inline'
                    )
                ),
                Field('email', css_class='input-hg'),
            ),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-primary btn-lg'),
                css_class='form-group'
            )
        )

        super(BaseAccountSettingsFields, self).__init__(*args, **kwargs)


@parsleyfy
class AccountSettingsForm(BaseAccountSettingsFields,
                          forms.ModelForm):

    class Meta:
        fields = ('first_name', 'last_name', 'email')
        model = User

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.user = self.request.user

        super(AccountSettingsForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        """
        save the requested email in the user.profile.data['validation_required_temp_email']
        send the confirmation email
        on reciept of the confirmation link click update the user email
        """
        profile = self.user.profile
        # salt and hash this thing
        temp_email = self.cleaned_data['email']

        # @TODO turn this into a reuseable function as its used in SignupForm too
        temp_email = User.objects.normalize_email(self.cleaned_data.get('email'))
        queryset = User.objects.exclude(pk=self.user.pk).filter(email=temp_email)

        try:
            existing_user = queryset.first()
        except AttributeError:
            try:
                existing_user = queryset[0]
            except IndexError:
                existing_user = None

        if existing_user is not None:
            raise forms.ValidationError("An account with that email already exists.")

        # detect a change
        if temp_email != self.user.email:
            profile.data['validation_required_temp_email'] = temp_email
            # require them to validate their email
            profile.validated_email = False
            profile.save(update_fields=['data'])

            m = ValidateEmailChangeMailer(
                    recipients=((self.user.get_full_name(), self.user.email, self.user),),)
            m.process(user=self.user)

            messages.warning(self.request, 'For your security you have been logged out. Please check your email address "%s" and click the email address change confirmation validation link' % self.request.user.email)
            logger.info(u'User: %s has requested a change of email address' % self.user)

            logout(self.request)

            # always return the current email address! we dotn want to change it
            # until the change has been confirmed
        return self.user.email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name != self.user.first_name:
            messages.success(self.request, 'Success. You have updated your First Name')
            return first_name
        return self.user.first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name != self.user.last_name:
            messages.success(self.request, 'Success. You have updated your Last Name')
            return last_name
        return self.user.last_name


@parsleyfy
class ChangePasswordForm(SetPasswordForm):
    title = "Change your password"

    old_password = forms.CharField(
        error_messages={
            'required': "Your current password cant be blank"
        },
        label='Current password',
        help_text='Once you have changed your password, you will be logged out and an email will be sent to your registered account for validation.',
        widget=forms.PasswordInput(attrs={'size': 30})
    )

    new_password1 = forms.CharField(
        error_messages={
            'required': "New password can't be blank."
        },
        label='New password',
        widget=forms.PasswordInput(attrs={'size': 30})
    )

    new_password2 = forms.CharField(
        error_messages={
            'required': "Verify password can't be blank."
        },
        label='Verify password',
        widget=forms.PasswordInput(attrs={
            'parsley-equalto': '[name="new_password1"]',
            'parsley-equalto-message': "The two password fields don't match.",
            'size': 30
        })
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.user = self.request.user

        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = self.action_url
        self.helper.form_show_errors = False
        self.helper.modal_form = True
        self.helper.attrs.update({'data-remote': 'true', 'parsley-validate': ''})

        self.helper.layout = Layout(
            Fieldset(
                '',
                Field('old_password', css_class='input-hg'),
            ),
            Fieldset(
                'New Password',
                Field('new_password1', css_class='input-hg'),
                Field('new_password2', css_class='input-hg'),
            ),
            ButtonHolder(
                Submit('submit', 'Change Password', css_class='btn btn-primary btn-lg'),
                css_class='form-group'
            )
        )

    @property
    def action_url(self):
        return reverse('me:change-password')

    def clean_old_password(self):
        if self.user.check_password(self.cleaned_data['old_password']) is not True:
            raise forms.ValidationError("Sorry, your old password is incorrect.")
        return self.cleaned_data['old_password']

    def clean_new_password2(self):
        """
        save the password salted and hashed in user.profile
        send the confirmation email
        on reciept of the confirmation link click only then update the user password
        """
        profile = self.user.profile

        new_password = self.cleaned_data['new_password2']

        # salt and hash this thing for comparison
        temp_password = make_password(new_password)

        profile.data['validation_required_temp_password'] = temp_password
        profile.save(update_fields=['data'])

        # send confirmation email
        m = ValidatePasswordChangeMailer(recipients=((self.user.get_full_name(), self.user.email, self.user),),)
        m.process(user=self.user)

        messages.warning(self.request, 'For your security you have been logged out. Please check your email address "%s" and click the change of password confirmation validation link' % self.request.user.email)
        logger.info(u'User: %s has requested a change of password' % self.user)

        logout(self.request)

        return new_password

    def save(self, *args, **kwargs):
        #
        # Do nothing here
        #
        pass

