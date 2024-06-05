from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_postal_code(value):
    if not value.isdigit():
        raise ValidationError(
            _("postal code must be a numerical")
        )