# -*- coding: utf-8 -*-
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, UpdateView, TemplateView

# from dj_authy.views import HoldingPageView, ProfileView

from pinax.stripe.models import Charge, Customer

from beer.mixins import AjaxFormView, AjaxModelFormView, ModalView


from .forms import (AccountSettingsForm,
                    PlanChangeForm,
                    AccountCancelForm)

import logging
logger = logging.getLogger('django.request')

User = get_user_model()


class AccountSettingsView(UpdateView):
    form_class = AccountSettingsForm
    model = User
    success_url = reverse_lazy('me:settings')
    template_name = 'user/settings/account.html'

    def get_form_kwargs(self):
        kwargs = super(AccountSettingsView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request
        })
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user


class PaymentListView(ListView):
    template_name = 'me/payment_list.html'

    def get_queryset(self):
        try:
            return Charge.objects.filter(customer=self.request.user.customer).order_by('-created_at')
        except Customer.DoesNotExist:
            return Charge.objects.none()


class PlanListView(TemplateView):
    template_name = 'me/plan_list.html'

    def get_context_data(self, **kwargs):
        context = super(PlanListView, self).get_context_data(**kwargs)
        context.update({
            'object_list': [settings.PAYMENTS_PLANS['early-bird-monthly'],]
        })
        return context


class PlanChangeView(ModalView, AjaxFormView, FormView):
    form_class = PlanChangeForm
    template_name = 'me/plan_change.html'

    def get_initial(self):
        return {
            'plan': self.kwargs.get('plan', None)
        }

    def form_valid(self, form):
        form.save()
        return super(PlanChangeView, self).form_valid(form)

    def get_object(self, **kwargs):
        slug = self.kwargs.get('plan', None)
        try:
            obj = settings.PAYMENTS_PLANS[slug]
        except KeyError:
            raise Http404("No plan found matching the id: {0}".format(slug))
        return obj

    def get_form_kwargs(self):
        kwargs = super(PlanChangeView, self).get_form_kwargs()
        kwargs.update({
            'plan': self.get_object(),
            'user': self.request.user,
        })
        return kwargs

    def get_success_url(self):
        return reverse('me:welcome')


# class TwoFactorDisableView(AjaxFormView, TemplateView):
#     template_name = 'user/settings/two_factor_confirm_disable.html'

#     def disable(self, request, *args, **kwargs):
#         profile = self.request.user.profile
#         profile.data['two_factor_enabled'] = False
#         profile.save(update_fields=['data'])

#         # messages.success(self.request, 'You have successfully disabled two-step verification for your LawPal account.')

#         return HttpResponseRedirect(self.get_success_url())

#     def post(self, request, *args, **kwargs):
#         return self.disable(request, *args, **kwargs)

#     def get_success_url(self):
#         return reverse('me:settings')


# class TwoFactorEnableView(AjaxModelFormView, ProfileView):
#     template_name = 'user/settings/two_factor_enable.html'

#     def get_success_url(self):
#         return reverse('me:two-factor-verify')

#     def form_valid(self, form):
#         super(TwoFactorEnableView, self).form_valid(form)

#         data = {
#             'modal': True,
#             'target': '#verify-two-factor',
#             'url': self.get_success_url()
#         }

#         return self.render_to_json_response(data)


# class TwoFactorVerifyView(AjaxFormView, HoldingPageView):
#     template_name = 'user/settings/two_factor_verify.html'

#     def form_valid(self, form):
#         profile = self.request.user.profile
#         profile.data['two_factor_enabled'] = True
#         profile.save(update_fields=['data'])

#         # messages.success(self.request, 'You have successfully enabled two-step verification for your LawPal account.')

#         return super(TwoFactorVerifyView, self).form_valid(form)

#     def get_success_url(self):
#         return reverse('me:settings')


class AccountCancelView(ModalView, AjaxFormView, FormView):
    form_class = AccountCancelForm

    def form_valid(self, form):
        form.save()
        logout(self.request)
        return super(AccountCancelView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(AccountCancelView, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs

    def get_success_url(self):
        return reverse('public:welcome')


class WelcomeView(TemplateView):
    template_name = 'me/welcome.html'
