from django.core.validators import RegexValidator

no_slash_validator = RegexValidator(
    regex=r"^[^/]*$",
    message="Slash (/) characters are not allowed.",
)
