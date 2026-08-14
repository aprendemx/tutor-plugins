from tutor import hooks
hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "mfe-lms-common-settings",
            """
MFE_CONFIG["LOGO_URL"] = "https://aprende.gob.mx/images/logo.png"
MFE_CONFIG["LOGO_TRADEMARK_URL"] = "https://aprende.gob.mx/images/logo.png"
MFE_CONFIG["LOGO_WHITE_URL"] = "https://aprende.gob.mx/images/logo.png"
MFE_CONFIG["FAVICON_URL"] = "https://aprende.gob.mx/images/favicon.ico"
    """
        )
    ]
)

