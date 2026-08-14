from tutor import hooks
hooks.Filters.ENV_PATCHES.add_item(
    (
        "openedx-lms-common-settings",
        "FEATURES['REQUIRE_COURSE_EMAIL_AUTH'] = True"
    )
)
