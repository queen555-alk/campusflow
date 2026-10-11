"""Input validation helpers."""


def clean_choice(value, options, label):
    for option in options:
        if str(value).strip().lower() == option.lower():
            return option
    raise ValueError(f"Invalid {label} '{value}'. Choose from: {', '.join(options)}.")


def clean_title(value):
    value = str(value).strip()
    if not value:
        raise ValueError("Title must not be blank.")
    return value


def clean_users(value):
    value = str(value).strip()
    if not value.isascii() or not value.isdigit() or int(value) < 1:
        raise ValueError(
            f"Affected users must be a positive whole number (got '{value}')."
        )
    return int(value)
