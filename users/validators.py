import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_name(value):
    # Regex pattern to match only English and Arabic characters
    name_regex = r'^[A-Za-z\u0621-\u064A\u0660-\u0669]+$'

    # Check if the value matches the pattern
    if not re.match(name_regex, value):
        raise ValidationError(
            _("This field can only contain English and Arabic characters."))


def validate_username(value):
    # Regex pattern to validate username without length restriction
    # Only allows alphanumeric characters, underscores, and hyphens
    username_regex = r'^[A-Za-z0-9_-]+$'

    # Check if the value matches the pattern
    if not re.match(username_regex, value):
        raise ValidationError(
            _("Username must be alphanumeric, with underscores or hyphens."))
