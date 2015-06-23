# -*- coding: utf-8 -*-
from django.forms.forms import BaseForm
from django.views.generic.base import View

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit


class ModalForm(BaseForm):
    """
    A mixin that sets up a Form to be displayed in a modal dialog.
    """
    def __init__(self, *args, **kwargs):
        super(ModalForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = self.action_url
        self.helper.form_show_errors = False
        self.helper.modal_form = True

        self.helper.attrs.update({'data-remote': 'true', 'parsley-validate': ''})

        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-default', data_dismiss='modal'))

        if getattr(self, 'show_action', True) is True:
            self.helper.add_input(Submit('submit', 'Submit', css_class='btn-wide'))

    @property
    def action_url(self):
        raise NotImplementedError

    @property
    def title(self):
        raise NotImplementedError


class ModalView(View):
    """
    A mixin that sets the correct template for modal based views.
    """
    template_name = 'modal.html'
