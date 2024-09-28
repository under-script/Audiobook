from .base import *

DATABASES = {
    'default': env.db(),
    'extra': env.db_url(
        'DATABASE_URL',
        default=env('DATABASE_URL'),
        engine=env('SQL_ENGINE')
    )
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
TIME_ZONE = 'Asia/Tashkent'