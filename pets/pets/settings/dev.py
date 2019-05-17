from .prod import *  # noqa: F403

INSTALLED_APPS += ("debug_toolbar", "test_without_migrations")

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda r: config("SHOW_DEBUG_TOOLBAR", default="False", cast=bool)
}

TEMPLATES[0]["OPTIONS"]["loaders"] = PROJECT_TEMPLATE_LOADERS

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
