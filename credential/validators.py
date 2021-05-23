from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class MinIntValidator(MinValueValidator):
    def clean(self, value):
        if not value.isdigit():
            self.raise_error(value)

        try:
            cleaned = int(value)
        except ValueError:
            self.raise_error(value)
        else:
            return cleaned

    def raise_error(self, value):
        message = _("Ensure %(value)s is integer")
        code = "invalid"
        params = {"value": value}
        raise ValidationError(message, code, params)
