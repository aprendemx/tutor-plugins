from tutor import hooks

# 1) Activa CORS headers en el LMS
hooks.Filters.ENV_PATCHES.add_item((
    "lms-env",
    'FEATURES["ENABLE_CORS_HEADERS"] = True',
))
# 2) Permite orígenes cruzados: tu localhost y la IP de la VM
hooks.Filters.ENV_PATCHES.add_item((
    "lms-env",
    'CORS_ORIGIN_WHITELIST = ["http://localhost:8000", "http://20.64.89.2"]',
))
# 3) Confía en esos mismos orígenes para CSRF
hooks.Filters.ENV_PATCHES.add_item((
    "lms-env",
    'CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://20.64.89.2"]',
))

