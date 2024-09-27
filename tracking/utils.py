import random
import string


async def generate_tracking_number():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=16))
