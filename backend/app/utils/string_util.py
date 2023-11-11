import random
import string


def random_string(length: int = 10) -> str:
    """
    Generate a random string of fixed length 
    """
    chars = string.ascii_letters + string.digits
    
    return "".join(random.choice(chars) for _ in range(length))
