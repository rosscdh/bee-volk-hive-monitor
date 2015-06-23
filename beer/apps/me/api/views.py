# -*- coding: UTF-8 -*-
from django.core import signing
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import generics
from rest_framework import status as http_status
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from password_reset.views import SaltMixin

from .serializers import (UserSerializer,
                          ChangePasswordSerializer,
                          ForgotPasswordSerializer)


class ChangePasswordView(APIView):
    def post(self, request):
        ser = ChangePasswordSerializer(data=self.request.data, context={'request': self.request})
        if ser.is_valid(True):
            user = self.request.user
            user.set_password(ser.validated_data['new_password'])
            user.save(update_fields=['password'])
        return Response()


class MeView(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self, *args, **kwargs):
        # filter the scans based on the current project -
        return self.model.objects.get(pk=self.request.user.pk)


class UserViewSet(SaltMixin, viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def __init__(self, **kwargs):
        super(UserViewSet, self).__init__(**kwargs)

    def get_queryset(self):
        query = User.objects.filter(client=self.request.user.client)
        # filter out is_staff users (for now?) to avoid them showing up in the list of "users" that a
        # client sees.  this will happen when the STE is in the company, validating equipment and such
        query = query.filter(is_staff=False)
        #
        return query

    def perform_create(self, serializer):
        # company is hidden from the user, not in the json, etc.  one user is always attached
        # to ONE company at a time.  During creation we force this to the users active company.id
        serializer.save(client=self.request.user.company)

    # unfortunately, at this point we can't fix the URL (needs newer django), url_path="reset-password"
    @detail_route(methods=['POST'])
    def reset_password(self, request, **kwargs):  # kwargs contains the
        """
        Sends the "reset your password" email to the user
        """
        # As a user
        # I need to be able to recieve and email with a reset password token
        # hould I foget my password.
        # So that I can continue to use the system without a problem
        user = self.get_object()
        context = {
            'site': RequestSite(self.request),
            'user': user,
            'token': signing.dumps(user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }
        # body = loader.render_to_string(self.email_template_name, context).strip()
        # subject = loader.render_to_string(self.email_subject_template_name, context).strip()
        # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        m = ForgotPasswordEmail(recipients=((user.get_full_name(), user.email, user),))
        m.process(**context)
        return Response("OK")


class RegisterView(generics.CreateAPIView):
    """
    Allow new users to register with us.
    Clients must pass in:

    activation_link: "http://url.for.your.client.service/path/to/validate/:token"

    This will then be injected into the email with a secure token genrated on our side
    """
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # allow any only for registration, relies on CORS

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        user = None
        try:
            with transaction.commit_on_success():
                email = data.pop('email', None)
                password = data.pop('password', None)
                company = data.pop('company', {})

                try:
                    user, is_new = self.model.objects.create_api_user(email=email, password=password, company=company,
                                                                      **data)
                except self.model.objects.CompanyAlreadyExistsException as e:
                    return Response({'error': unicode(e)}, status=http_status.HTTP_406_NOT_ACCEPTABLE)

                # dont allow the email to be reused
                if is_new is False:
                    data = {'error': 'Email is already registered'}
                    status_code = http_status.HTTP_406_NOT_ACCEPTABLE
                else:
                    serializer = self.serializer_class(user)
                    # populate the data and set status
                    data = serializer.data
                    status_code = http_status.HTTP_201_CREATED

        except Exception as e:
            status_code = http_status.HTTP_400_BAD_REQUEST
            data = {'error': str(e)}

        return Response(data, status=status_code)


class VerifyUserView(generics.CreateAPIView):
    """
    Allow new users to be verified.
    Clients must pass in:

    token: "TOKEN_THAT_WAS_PROVIDED_IN_WELCOME_EMAIL"
    """
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # allow any only for registration, relies on CORS

    def get_user(self, token):
        try:
            pk = signing.loads(token, salt=settings.URL_ENCODE_SECRET_KEY)
        except signing.BadSignature:
            raise Http404
        return get_object_or_404(User, pk=pk)

    def post(self, request, *args, **kwargs):
        try:
            self.user = self.get_user(token=request.data.get('token'))
        except User.DoesNotExist:
            raise Http404

        return Response({"message": "User %s Validated" % self.user.email}, status=http_status.HTTP_200_OK)


class ForgotPasswordView(SaltMixin, APIView):
    """
    As a user
    I need to be able to recieve and email with a reset password token
    should I foget my password.
    So that I can continue to use the system without a problem
    """
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)  # allow any only for non-loggedin, relies on CORS

    template_name = 'password_reset/recovery_form.html'
    email_template_name = 'password_reset/recovery_email.txt'
    email_subject_template_name = 'password_reset/recovery_email_subject.txt'
    case_sensitive = True
    search_fields = ['email']

    def send_notification(self, user):
        context = {
            'site': RequestSite(self.request),
            'user': user,
            'token': signing.dumps(user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }
        # body = loader.render_to_string(self.email_template_name, context).strip()
        # subject = loader.render_to_string(self.email_subject_template_name, context).strip()
        # send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
        m = ForgotPasswordEmail(recipients=((user.get_full_name(), user.email, user),))
        m.process(**context)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        email = data.get('email', None)
        data['username_or_email'] = email

        form = PasswordRecoveryForm(data=data,
                                    case_sensitive=self.case_sensitive,
                                    search_fields=self.search_fields)
        if form.is_valid() is False:
            # handle errors
            data = {'errors': form.errors.get('username_or_email', ['Unknown'])}
            status_code = http_status.HTTP_404_NOT_FOUND
        else:
            self.send_notification(user=form.get_user_by_email(email))
            data = {'message': 'Successfully sent reset password email.'}
            status_code = http_status.HTTP_200_OK

        return Response(data, status=status_code)