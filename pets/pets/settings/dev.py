from .prod import *

DEBUG = True

INSTALLED_APPS += ('debug_toolbar', 'test_without_migrations')
