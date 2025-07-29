from odoo.fields import Date


def date_validator(field, value, error):
    try:
        Date.from_string(value)
    except ValueError:
        return error(field, "{} does not match format '%Y-%m-%d'".format(value))


def boolean_validator(field, value, error):
    if value and value not in ["true", "false"]:
        error(field, "Must be a boolean value: true or false")
