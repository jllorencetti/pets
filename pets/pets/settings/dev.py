from .prod import *  # noqa: F403

INSTALLED_APPS += (
    'debug_toolbar',
    'test_without_migrations',
)

TEMPLATES[0]['OPTIONS']['loaders'] = PROJECT_TEMPLATE_LOADERS

MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
