# -*- coding: utf-8 -*-
from django.contrib.auth import logout


class LogOutMixin(object):
    """
    Mixin that will log the current user out
    and continue showing the view as an non authenticated user
    """
    def dispatch(self, request, *args, **kwargs):
        """
        If the user is logged in log them out
        """
        if request.user.is_authenticated() is True:
            logout(request)

        return super(LogOutMixin, self).dispatch(request, *args, **kwargs)
