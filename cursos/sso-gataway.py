from tutor import hooks

# Registrar variables en config.yml con defaults vacíos
hooks.Filters.CONFIG_DEFAULTS.add_items([
    ("SSO_GATEWAY_SABERES_PUBLIC_KEY", ""),
    ("SSO_GATEWAY_CLIENT_DOMAINS", []),
])

hooks.Filters.ENV_PATCHES.add_item((
    "openedx-lms-common-settings",
    """
# SSO Gateway Configuration
SSO_GATEWAY_SABERES_PUBLIC_KEY = {{ SSO_GATEWAY_SABERES_PUBLIC_KEY | tojson }}

_SSO_GATEWAY_DOMAINS = {{ SSO_GATEWAY_CLIENT_DOMAINS | tojson }}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST)
for _domain in _SSO_GATEWAY_DOMAINS:
    if _domain not in CORS_ORIGIN_WHITELIST:
        CORS_ORIGIN_WHITELIST.append(_domain)

CSRF_TRUSTED_ORIGINS = list(CSRF_TRUSTED_ORIGINS)
for _domain in _SSO_GATEWAY_DOMAINS:
    _host = _domain.replace("https://", "").replace("http://", "")
    if _host not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_host)

LOGIN_REDIRECT_WHITELIST = list(LOGIN_REDIRECT_WHITELIST)
for _domain in _SSO_GATEWAY_DOMAINS:
    _host = _domain.replace("https://", "").replace("http://", "")
    if _host not in LOGIN_REDIRECT_WHITELIST:
        LOGIN_REDIRECT_WHITELIST.append(_host)
    """,
))
