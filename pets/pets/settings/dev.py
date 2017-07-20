from model_mommy import generators

from .prod import *

INSTALLED_APPS += ('debug_toolbar', 'test_without_migrations')

MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES

TEMPLATES[0]['OPTIONS']['loaders'] = PROJECT_TEMPLATE_LOADERS

MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.fields.AutoSlugField': generators.gen_slug,
}
