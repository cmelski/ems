import random
import string


def generate_random_string():
    random_string = ''.join(random.choices(string.ascii_letters, k=10))
    return random_string
