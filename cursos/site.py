from tutor import hooks
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-common-settings",
        "SITE_ID = 18"
    )
)


