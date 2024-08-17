from find_job.settings import *
from decouple import config



SECRET_KEY = config('SECRET_KEY')


ALLOWED_HOSTS = ['web-production-262c.up.railway.app']


CSRF_TRUSTED_ORIGINS = [
    'https://web-production-262c.up.railway.app',
]