from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a Limiter instance for rate limiting
limiter = Limiter(key_func=get_remote_address)