from tutor import hooks
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "GRADEBOOK_FREEZE_DAYS = 30"
    )
)
