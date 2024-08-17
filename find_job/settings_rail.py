from find_job.settings import *
from decouple import config



SECRET_KEY = config('SECRET_KEY')



ALLOWED_HOSTS = ['web-production-262c.up.railway.app', '127.0.0.1']


CSRF_TRUSTED_ORIGINS = [
    'https://web-production-262c.up.railway.app',
     "http://localhost:3000",
]