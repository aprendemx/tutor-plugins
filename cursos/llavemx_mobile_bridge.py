from tutor import hooks

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
