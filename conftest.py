import os

import django
import pytest
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'task_manager.settings'
django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'ATOMIC_REQUESTS': True,
    }