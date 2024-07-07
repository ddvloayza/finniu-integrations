import random
import string
from datetime import date


def generate_random_letter(salt=4):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(salt))


def date_string():
    return date.today().strftime("%Y-%m-%d")
