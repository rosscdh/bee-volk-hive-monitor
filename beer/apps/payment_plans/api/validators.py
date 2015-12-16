from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError


class FieldsAreEqualValidator:
    message = _('Fields do not match.')
    missing_message = _('This field is required.')

    def __init__(self, primary, secondary, message=None):
        """
        Checks that two fields are equal.  The error message is applied to the 'secondary' field.  Both fields
        should be marked as 'required'.  The required validation will be performed first
        :param primary: The primary field to validate
        :param secondary: The secondary field to validate matches the primary field
        :param message: Error message to show
        """
        self.primary = primary
        self.secondary = secondary
        if message:
            self.message = _(message)

    def __call__(self, attrs):
        if attrs[self.primary] != attrs[self.secondary]:
            raise ValidationError({
                self.secondary: [self.message]
            })

