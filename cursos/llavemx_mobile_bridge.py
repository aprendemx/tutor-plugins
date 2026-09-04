from tutor import hooks

# Las cinco variables que consume el patch. Sin esto, cualquier instancia que
# no las tenga escritas a mano en config.yml falla al renderizar con
# "Missing configuration value". Producción funciona solo porque alguien las
# puso ahí en su momento.
hooks.Filters.CONFIG_DEFAULTS.add_items([
    ("LLAVEMX_MOBILE_CLIENT_ID", ""),
    ("LLAVEMX_TOKEN_URL", ""),
    ("LLAVEMX_USER_INFO_URL", ""),
    ("LLAVEMX_ANDROID_DEEP_LINK_SCHEME", ""),
    ("LLAVEMX_IOS_DEEP_LINK_SCHEME", ""),
])

hooks.Filters.ENV_PATCHES.add_item((
    "openedx-lms-common-settings",
    """
# LlaveMX Mobile Bridge Configuration
LLAVEMX_MOBILE_CLIENT_ID          = "{{ LLAVEMX_MOBILE_CLIENT_ID }}"
LLAVEMX_TOKEN_URL                 = "{{ LLAVEMX_TOKEN_URL }}"
LLAVEMX_USER_INFO_URL             = "{{ LLAVEMX_USER_INFO_URL }}"
LLAVEMX_ANDROID_DEEP_LINK_SCHEME  = "{{ LLAVEMX_ANDROID_DEEP_LINK_SCHEME }}"
LLAVEMX_IOS_DEEP_LINK_SCHEME      = "{{ LLAVEMX_IOS_DEEP_LINK_SCHEME }}"
    """,
))
