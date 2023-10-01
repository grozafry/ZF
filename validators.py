import re
from django.core.exceptions import ValidationError

def validate_mobile_number(value):
    pattern = r'^\d{10}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid mobile number format. Please enter a 10-digit number.')