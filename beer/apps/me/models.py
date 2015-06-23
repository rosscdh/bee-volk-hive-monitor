# -*- coding: utf-8 -*-
from django.db import models

from .mixins import EmailIsValidatedMixin
from django.contrib.auth.models import User
from jsonfield import JSONField

import logging
logger = logging.getLogger('django.request')


class UserProfile(EmailIsValidatedMixin, models.Model):
    """
    Base User Profile, where we store all the interesting information about
    users
    """
    has_notifications = models.BooleanField(default=False)

    user = models.OneToOneField('auth.User',
                                unique=True,
                                related_name='profile')

    data = JSONField(default={})

    @classmethod
    def create(cls, **kwargs):
        profile = cls(**kwargs)
        profile.save()
        return profile

    def __unicode__(self):
        return '%s <%s>' % (self.user.get_full_name(), self.user.email)


def _get_or_create_user_profile(user):
    # set the profile
    # This is what triggers the whole cleint profile creation process in pipeline.py:ensure_user_setup
    try:
        profile, is_new = UserProfile.objects.get_or_create(user=user)  # added like this so django noobs can see the result of get_or_create
        return (profile, is_new,)

    except Exception as e:
        logger.critical('transaction.atomic() integrity error: %s' % e)

    return (None, None,)


# used to trigger profile creation by accidental refernce. Rather use the _create_user_profile def above
User.add_to_class('profile', property(lambda u: _get_or_create_user_profile(user=u)[0]))


def custom__unicode__(self, **kwargs):
    """
    Overide the user __unicode__ method to actually return somethign useful.
    """
    name = '%s %s' % (self.first_name, self.last_name)
    if name.strip() in ['', None]:
        name = self.email
    return name

User.add_to_class('__unicode__', custom__unicode__)


def get_full_name(self, **kwargs):
    """
    Overide the user get_full_name method to actually return somethign useful if
    there is no name.

    Used to return the email address as their name, if no first/last name exist.
    """
    name = '%s %s' % (self.first_name, self.last_name)
    if name.strip() in ['', None]:
        name = self.email
    return name

User.add_to_class('get_full_name', get_full_name)


def get_initials(self):
    """
    Add in the get_initials method, which returns the user initials based on their
    first and last name
    """
    initials = None
    try:
        initials = '%s%s' % (self.first_name[0], self.last_name[0])
        initials = initials.strip().upper()
    except IndexError:
        pass

    if initials in ['', None]:
        return None
    return initials

User.add_to_class('get_initials', get_initials)
