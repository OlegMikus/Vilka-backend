from src.config.constants import DB_URL

TORTOISE_MODULES = {
    'user': ['src.db.models'],
}

TORTOISE_APPS = {
    'user': {
        'models': ['src.db.models', 'aerich.models'],
        'default_connection': 'default',
    },
}

TORTOISE_ORM = {
    'connections': {'default': DB_URL},
    'apps': TORTOISE_APPS,
}
