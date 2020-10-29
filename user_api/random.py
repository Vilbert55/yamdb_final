import random
import string


def text_gen(k):
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=k))
    return text
