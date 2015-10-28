# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import UpdateView, ListView, DetailView

from formtools.wizard.views import SessionWizardView

from .models import Bet, DonationRecipient
from .forms import BetFormStart, BetFormDonationRecipient, BetFormUserInfo, ShareForm
from .api.serializers import DonationRecipientSerializer


class BetListView(ListView):
    """
    """
    model = Bet


def show_donation_recipient_form(wizard):
    """Return true if user opts to pay by credit card"""
    # Get cleaned data from payment step
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {'donation_recipient': None}
    return cleaned_data.get('donation_recipient') is None


def show_user_info_form(wizard):
    """
    """
    return wizard.request.user.is_authenticated() is False


class BetCreateView(SessionWizardView):
    """
    """
    TEMPLATES = {
        '0': 'bet/bet_form_with_donation_recipients.html'
    }

    condition_dict = {
        '1': show_donation_recipient_form,
        '2': show_user_info_form,
    }
    form_list = [BetFormStart, BetFormDonationRecipient, BetFormUserInfo]

    # form_dict = {'bet': BetFormStart,
    #              'recipient': BetFormDonationRecipient,
    #              'user': BetFormUserInfo,}

    template_name = 'bet/bet_form.html'

    def get_template_names(self):
        try:
            return [self.TEMPLATES[self.steps.current]]
        except:
            return self.template_name

    def get_success_url(self):
        return reverse('bet:detail', kwargs={'slug': self.bet.slug})

    def done(self, form_list, form_dict, **kwargs):
        self.bet, is_new = form_dict['0'].save()

        if '1' in form_dict.keys() and form_dict['1'].is_valid():
            donation_recipient = form_dict['1'].save()
        else:
            donation_recipient = DonationRecipient.objects.get(pk=form_dict['0'].cleaned_data.get('donation_recipient'))

        if '2' in form_dict.keys() and form_dict['2'].is_valid():
            user, is_new = form_dict['2'].save()
            # Log the user in
            user = authenticate(username=user.username,
                                password=form_dict['2'].cleaned_data.get('password'))
            login(self.request, user)
        else:
            user = self.request.user

        # save the user associated with this bet
        self.bet.user = user
        self.bet.save(update_fields=['user'])
        self.bet.recipients.add(donation_recipient)

        return redirect(self.get_success_url())


class CloneBetFormView(BetCreateView):
    """
    Same functioanlity as create
    """

    def get_form_initial(self, step):
        self.bet_to_clone = Bet.objects.get(slug=self.kwargs.get('slug'))
        initial = super(CloneBetFormView, self).get_form_initial(step=step)
        if step == '0':
            initial.update({
                'name': self.bet_to_clone.name,
                'description': self.bet_to_clone.description,
                'amount': self.bet_to_clone.amount,
                'donation_recipient': self.bet_to_clone.recipients.all().first().pk,
            })

        return initial

    def done(self, *args, **kwargs):
        redirect = super(CloneBetFormView, self).done(*args, **kwargs)

        # Setup the clone variables
        self.bet.parent_bet = self.bet_to_clone
        self.bet.sub_bet_type = Bet.SUB_BET_TYPE.clone
        self.bet.save(update_fields=['parent_bet', 'sub_bet_type'])
        # redirect
        return redirect


class BetDetailView(DetailView):
    """
    """
    model = Bet

    def user_has_cloned_bet(self):
        return self.object.bet_set.filter(user=self.request.user).count() == 1

    def get_context_data(self, *args, **kwargs):
        context = super(BetDetailView, self).get_context_data(*args, **kwargs)
        url = self.request.build_absolute_uri()
        context.update({
            'facebook_share_form': ShareForm(initial={'text': 'facebook share content here: %s' % url}),
            'twitter_share_form': ShareForm(initial={'text': 'twitter share content here: %s' % url}),
            'donation_recipients': DonationRecipientSerializer(self.object.recipients.all(), many=True).data
        })
        return context


class BetFormView(UpdateView):
    """
    """
    model = Bet
    form_class = BetFormStart
    template_name = 'bet/bet_form.html'


class CounterBetFormView(BetFormView):
    def get_initial(self):
        initial = super(CounterBetFormView, self).get_initial()
        initial.update({'parent_bet': self.get_object()})
        return initial
