from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.http import HttpResponseServerError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit

from decorator import decorator

import json


@decorator
def json_response(function=None, *args, **kwargs):
    try:
        response = function(*args, **kwargs)
    except Exception as e:
        error = {
            'error': {
                'message': unicode(e)
            }
        }
        response = HttpResponseServerError()
        response.content = json.dumps(error, separators=(',', ':'))

    response['Content-Type'] = 'application/json'
    return response


class JSONResponseMixin(object):
    def render_to_json_response(self, context, **kwargs):
        return self.get_json_response(self.convert_context_to_json(context), **kwargs)

    def get_json_response(self, content, **kwargs):
        return HttpResponse(content, content_type='application/json', **kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)


class AjaxFormViewMixin(object):
    """
    A mixin that handles form submission over AJAX.
    """
    @json_response
    def post(self, request, *args, **kwargs):
        return super(AjaxFormViewMixin, self).post(request)

    @json_response
    def put(self, request, *args, **kwargs):
        return super(AjaxFormViewMixin, self).put(request)


class AjaxValidFormViewMixin(JSONResponseMixin,
                             AjaxFormViewMixin):
    """
    A mixin that handles successful AJAX form submissions for simple
    FormView based views.
    """
    def form_valid(self, form):
        data = {
            'redirect': True,
            'url': self.get_success_url()
        }

        return self.render_to_json_response(data)


class AjaxValidModelFormViewMixin(JSONResponseMixin,
                                  AjaxFormViewMixin):
    """
    A mixin that handles successful AJAX form submissions for views
    that use a Django ModelForm.
    """
    def form_valid(self, form):
        self.object = form.save()

        data = {
            'redirect': True,
            'url': self.get_success_url()
        }

        return self.render_to_json_response(data)


class AjaxInvalidFormViewMixin(JSONResponseMixin,
                               AjaxFormViewMixin):
    """
    A mixin that handles invalid AJAX form submissions for FormView based views.
    """
    def form_invalid(self, form):
        errors = form.errors['__all__'] if '__all__' in form.errors else form.errors
        data = {
            'errors': errors
        }
        return self.render_to_json_response(data, status=400)


class AjaxFormView(AjaxValidFormViewMixin,
                   AjaxInvalidFormViewMixin,
                   FormView):
    """
    A mixin that handles AJAX form submissions for FormView based views.

    See: https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-editing/#basic-forms
    """
    pass


class AjaxModelFormView(AjaxValidModelFormViewMixin,
                        AjaxInvalidFormViewMixin,
                        FormView):
    """
    A mixin that handles AJAX form submissions for views that use a ModelForm.

    See: https://docs.djangoproject.com/en/1.6/topics/class-based-views/generic-editing/#model-forms
    """
    pass
