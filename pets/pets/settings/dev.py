from model_mommy import generators

from .prod import *

DEBUG = True

INSTALLED_APPS += ('debug_toolbar', 'test_without_migrations')

TEMPLATES[0]['OPTIONS']['loaders'] = PROJECT_TEMPLATE_LOADERS

MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.fields.AutoSlugField': generators.gen_slug,
}
