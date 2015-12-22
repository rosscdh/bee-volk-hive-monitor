# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from crispy_forms.layout import HTML, Layout

from pinax.stripe.forms import PlanForm
from pinax.stripe.models import Customer

from beer.mixins import ModalForm

import logging
logger = logging.getLogger('django.request')


User = get_user_model()


class PlanChangeForm(PlanForm, ModalForm):
    stripe_token = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, plan, user, *args, **kwargs):
        self.plan = plan
        self.user = user

        super(PlanChangeForm, self).__init__(*args, **kwargs)

        if self.user.profile.subscription:
            self.helper.attrs.update({'id': 'plan-change-form'})

            self.helper.layout = Layout(
                'plan',
                HTML('<p>Your monthly bill will increase from ${0} to ${1} on {2}.</p>'.format(
                    '25',
                    self.plan['price'],
                    '18 April, 2014'
                )),
                HTML('<p><strong>Plan changes are immediate.</strong></p>'),
                # Yes, change my plan
            )
        else:
            self.helper.attrs.update({'id': 'subscribe-form'})
            del self.helper.attrs['data-remote']

            self.helper.layout = Layout(
                'plan',
                'stripe_token',
                HTML('<p class="lead"><strong>Thank you for choosing LawPal. We will charge your card ${0} on the {1} of every month starting on {2}.</strong></p><p>If you change your mind, you can cancel your account at any time.</p> '.format(
                    self.plan['price'],
                    '{% now "jS" %}',
                    '{% now "F j, Y" %}'
                )),
                HTML('<p>We will email you a receipt each time. You can always upgrade, downgrade, or cancel any time.</p>'),
                # Subscribe
            )

        self.fields['plan'].widget = forms.HiddenInput()

    def save(self, **kwargs):
        # try:
        try:
            customer = self.user.customer
        except ObjectDoesNotExist:
            customer = Customer.create(self.user)
        finally:
            if self.cleaned_data['stripe_token'] not in [None, '']:
                customer.update_card(self.cleaned_data['stripe_token'])
            customer.subscribe(self.cleaned_data['plan'])
        # except stripe.StripeError as e:
            # print e.args[0]

    @property
    def action_url(self):
        return reverse('payment_plans:plan-change', kwargs={'plan':self.plan['stripe_plan_id']})

    @property
    def title(self):
        if self.user.profile.subscription:
            return 'Change to the {0} plan'.format(self.plan['name'])
        else:
            return 'Subscribe to the {0} plan'.format(self.plan['name'])


class AccountCancelForm(ModalForm, forms.Form):
    title = 'Is there anything we can do better? We want to help.'

    reason = forms.ChoiceField(
        choices=(
            ('', 'Select a reason...'),
            ('difficulty-of-use', 'Difficulty of use'),
            ('other', 'Other'),
        ),
        error_messages={
            'required': "Reason can't be blank."
        },
        label='Please tell us why you want to close your account:',
        help_text='',
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AccountCancelForm, self).__init__(*args, **kwargs)

    def save(self, **kwargs):
        # delete their subscription
        try:
            customer = self.user.customer
        except ObjectDoesNotExist:
            pass
        else:
            customer.cancel(at_period_end=False)

        # set the account to be inactive
        self.user.is_active = False
        self.user.save(update_fields=['is_active'])

        # analytics = AtticusFinch()
        # analytics.event('user.cancel', reason=self.cleaned_data.get('reason'), user=self.user)

    @property
    def action_url(self):
        return reverse('payment_plans:cancel')
