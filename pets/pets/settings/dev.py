from model_mommy import generators

from .prod import *

INSTALLED_APPS += ('test_without_migrations',)

TEMPLATES[0]['OPTIONS']['loaders'] = PROJECT_TEMPLATE_LOADERS

MOMMY_CUSTOM_FIELDS_GEN = {
    'autoslug.fields.AutoSlugField': generators.gen_slug,
}
