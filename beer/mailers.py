# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.translation import override, get_language
from templated_email import send_templated_mail

import logging
LOGGER = logging.getLogger('django.request')


class BaseMailerService(object):
    email_template = None
    base_email_template_location = 'email/'
    user = {
        "name": None,
        "email": None,
        "user_obj": None,
    }

    def __init__(self, recipients, from_tuple=None, subject=None, message=None, **kwargs):
        """
        subject : string
        message : string
        from_tuple : (:name, :email)
        recipients : ((:name, :email), (:name, :email),)
        """
        # Prepare the content
        self.subject = getattr(self, 'subject', subject)
        self.message = getattr(self, 'message', message)
        # Prepare receiver / sender infos
        self.from_tuple = self.make_from_tuple(from_tuple=from_tuple)
        self.recipients = self.prepare_recipients(recipients)

        # Do some final sanity checks to ensure that the constructed instance
        # can be used in a meaningful way.
        self.sanity_checks()

    #############
    # UTILITIES #
    #############
    def from_email(self, name=None, email=None):
        """
        from email must always come from the default site email to avoid being rejected
        but to handle this we set teh reply_to header to be the owner email
        """
        site_email = settings.DEFAULT_FROM[0][1]
        return '%s (via Scantrsut) %s' % (name, site_email) if email != site_email else email

    def make_from_tuple(self, from_tuple=None):
        """
        Constructs the sender information based on passed in from_tuple
        argument or default values frmo settings module.
        """
        return_tuple_dict = {}
        self.from_tuple = self.user.copy()  # setup the dictionary
        # if no from_tuple is provided simply use the defaults
        base_from_tuple = settings.DEFAULT_FROM[0]

        # Defaults to site name
        from_email = self.from_email(
            name=from_tuple[0] if from_tuple is not None else base_from_tuple[0],
            email=from_tuple[1] if from_tuple is not None else base_from_tuple[1]
        )

        return_tuple_dict.update({
            'name': from_tuple[0] if from_tuple is not None else base_from_tuple[0],  # default site from name
            'email': from_email,
            'reply_to': from_tuple[1] if from_tuple is not None else base_from_tuple[1]  # default is site email if no from_tuple has been specified
        })
        return return_tuple_dict

    def prepare_recipients(self, recipients):
        """
        Basically ensures that recipients are formatted the same way for
        later usage.

        recipients: arbitratry passed in receivers of the mail we want to
        send
        """
        final_list = []
        for r in recipients:
            u = self.user.copy()
            u.update({
                'name': r[0],
                'email': r[1],
                'user_obj': r[2],
            })
            final_list.append(u)
        return final_list

    def sanity_checks(self):
        """
        Small collection of assert statements that ensure the instance is in
        a usable state.
        """
        assert self.email_template  # defined in inherited classes
        assert self.from_tuple
        assert type(self.from_tuple) is dict
        assert self.recipients
        assert type(self.recipients) is list
        assert len(self.recipients) >= 1

    #################
    # FUNCTIONALITY #
    #################
    def process(self, attachments=None, **kwargs):
        self.params = kwargs

        for r in self.recipients:
            context = {
                'from': self.from_tuple.get('name'),
                'from_email': self.from_email(name=self.from_tuple.get('name'), email=self.from_tuple.get('email')),
                'recipient': r,
                'to': r.get('name'),
                'to_email': r.get('email'),
                'subject': self.subject,
                'message': self.message
            }

            LOGGER.debug('Email going out from: %s' % context.get('from_email'))

            context.update(**kwargs)

            return self.send_mail(context=context, attachments=attachments)

    def send_mail(self, context, attachments=None):

        return send_templated_mail(template_name=self.email_template,
                                   template_prefix=self.base_email_template_location,
                                   from_email=context.get('from_email'),
                                   recipient_list=[context.get('to_email')],
                                   bcc=[],
                                   context=context,
                                   attachments=attachments,
                                   headers={'Reply-To': self.from_tuple.get('reply_to')})


class BaseSpecifiedFromMailerService(BaseMailerService):
    """
    Require the code to pass in a from_tuple
    used for emails that are sent on behalf of the owner
    or some other user
    """
    def __init__(self, from_tuple, recipients, subject=None, message=None, **kwargs):
        # see how we require from_tuple and pass it in
        super(BaseSpecifiedFromMailerService, self).__init__(recipients=recipients, from_tuple=from_tuple, subject=subject, message=message, **kwargs)


class BaseTranslatedMailerService(BaseMailerService):
    """
    Renders the acutal content of an email according to the users configurated
    language.
    """
    def send_mail(self, context, attachments=None):
        recipient_obj = context.get('recipient').get('user_obj')
        # Default for all language settings is 'en'
        with override(recipient_obj.language):
            return super(BaseTranslatedMailerService, self).send_mail(context=context,
                                                                      attachments=attachments)
