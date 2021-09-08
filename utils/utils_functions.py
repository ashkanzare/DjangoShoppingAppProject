from random import choices
import string


def generate_random_string():
    chars = string.ascii_uppercase + string.digits
    return ''.join(choices(chars, k=8))

