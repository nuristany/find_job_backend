from find_job.settings import *
from decouple import config



SECRET_KEY = config('SECRET_KEY')


ALLOWED_HOSTS = ['']