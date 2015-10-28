# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

#from crispy_forms.helper import FormHelper

from .models import Bet, DonationRecipient

import uuid


def _user_exists(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def _get_unique_username(username):
    username = slugify(username)  # apply the transforms first so that the lookup acts on the actual username
    username = username[0:29]
    while _user_exists(username=username):
        username = '%s-%s' % (username, uuid.uuid4().get_hex()[:4])
        username = username[0:29]  # be aware of fencepost error here field limit is 30

    return username


class BetFormStart(forms.Form):
    name = forms.CharField(label='I swear that I will:')
    description = forms.CharField(label='A more detailed examination of the commitment:', widget=forms.Textarea)
    amount = forms.FloatField(initial=5.00)
    donation_recipient = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Media:
        css = {
            'all': ('//cdnjs.cloudflare.com/ajax/libs/select2/4.0.0/css/select2.min.css',)
        }
        js = {
            'js/project-list-app.js',
            '//cdnjs.cloudflare.com/ajax/libs/select2/4.0.0/js/select2.min.js',
        }

    # class Meta:
    #     model = Bet
    #     exclude = ('slug', 'uuid', 'parent_bet_id', 'created_at', 'updated_at')

    # @property
    # def helper(self):
    #     helper = FormHelper()
    #     helper.form_id = 'support-form'
    #     helper.form_class = 'form'
    #     helper.form_method = 'POST'
    #     return helper
    def save(self, *args, **kwargs):
        obj = Bet(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            amount=self.cleaned_data['amount'],
        )
        obj.save()
        is_new = True
        return (obj, is_new)


class BetFormDonationRecipient(forms.ModelForm):
    class Meta:
        model = DonationRecipient
        fields = ('name', 'url', 'description')


class BetFormUserInfo(forms.Form):
    name = forms.CharField(label='Your Name')
    email = forms.EmailField()
    password = forms.CharField(label='A password', widget=forms.PasswordInput)

    def save(self, *args, **kwargs):
        username = self.cleaned_data['email'].split('@')[0]
        obj, is_new = User.objects.get_or_create(username=_get_unique_username(username),
                                                 email=self.cleaned_data['email'])
        if is_new is True:
            name = self.cleaned_data['name'].split(' ')
            obj.first_name = name[0]
            obj.last_name = ' '.join(name[1:])
            obj.set_password(self.cleaned_data['password'])
            obj.save(update_fields=['first_name', 'last_name', 'password'])

        return (obj, is_new)


class ShareForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)


class CanModifyForm(forms.Form):
    password = forms.CharField()

    def __init__(self, bet, *args, **kwargs):
        self.bet = bet
        super(CanModifyForm, self).__init__(*args, **kwargs)

    def validate_password(self, value):
        if self.bet.slug != value:
            forms.ValidationError('Incorrect Password Please try again')
        return value
