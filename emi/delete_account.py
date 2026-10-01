from tutor import hooks

# EMI no permite que los usuarios borren su cuenta. Se desactiva en el LMS
# (la API) y en el MFE de cuenta (la sección). Ulmo convive con las dos
# formas del ajuste, FEATURES[...] y de primer nivel: se fijan ambas.
hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-lms-common-settings",
     "ENABLE_ACCOUNT_DELETION = False\nFEATURES['ENABLE_ACCOUNT_DELETION'] = False"),
    ("mfe-lms-common-settings",
     'MFE_CONFIG["ENABLE_ACCOUNT_DELETION"] = False'),
])
