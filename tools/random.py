import random
import string

def create_rundom_string():
    length = 8
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return random_string