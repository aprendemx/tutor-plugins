from tutor import hooks
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "FEATURES['ENABLE_ACCOUNT_DELETION'] = False"
    )
)
