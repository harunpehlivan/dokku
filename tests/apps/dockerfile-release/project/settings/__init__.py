import os

environment = os.getenv('ENVIRONMENT')

if environment == 'dev':
    from .dev import *
elif environment in ['staging', 'production']:
    from .staging import *
else:
    raise Exception("Invalid environment")
