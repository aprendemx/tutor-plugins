from tutor import hooks

# --- 1) LMS: publicar y aceptar campos en el esquema de registro ---
# Usamos el hook correcto para settings del LMS (común a dev/prod).
# Ref: hooks + ENV_PATCHES en Tutor. 
hooks.Filters.ENV_PATCHES.add_item((
    "openedx-lms-common-settings",
    """
# === campos-extras: publicar campos extra (formato legacy) ===
try:
    REGISTRATION_EXTRA_FIELDS
except NameError:
    REGISTRATION_EXTRA_FIELDS = {}

# Columnas reales en auth_userprofile (tu BD las tiene)
REGISTRATION_EXTRA_FIELDS["phone_number"] = "optional"
REGISTRATION_EXTRA_FIELDS["state"] = "optional"

# Personalizados -> se guardarán como User Attributes mediante Extension Form
for _k in ['first_lastname','second_lastname','municipality','school_name','grade','cct','curp']:
    REGISTRATION_EXTRA_FIELDS[_k] = 'optional'

# Apuntar al Registration Extension Form que hará la persistencia
REGISTRATION_EXTENSION_FORM = "emi_registration.forms.RegistrationExtensionForm"

# === campos-extras: registrar la app del formulario extendido ===
# Antes vivía en env/apps/openedx/settings/lms/99-emi_registration.py, un
# archivo puesto a mano dentro de un directorio que Tutor regenera.
if "emi_registration" not in INSTALLED_APPS:
    INSTALLED_APPS += ("emi_registration",)
ENABLE_DYNAMIC_REGISTRATION_FIELDS = True
"""
))

# --- 2) (Opcional) Authn MFE: permitir que renderice dinámicamente lo publicado por el LMS ---
# Útil si NO hardcodeas inputs en el MFE. 
# Ref: discusiones sobre ENABLE_DYNAMIC_REGISTRATION_FIELDS en Authn MFE.
hooks.Filters.ENV_PATCHES.add_item((
    "mfe-lms-production-settings",
    '''
ENABLE_DYNAMIC_REGISTRATION_FIELDS = "true"
try:
    MFE_CONFIG["ENABLE_DYNAMIC_REGISTRATION_FIELDS"] = "true"
except Exception:
    MFE_CONFIG = {"ENABLE_DYNAMIC_REGISTRATION_FIELDS": "true"}
'''
))

# --- 3) Anunciar un mount para tu app local "emi_registration" ---
# Necesitarás ejecutar "tutor mounts add ~/emi_registration" (abajo).
# Ref: ejemplo de MOUNTED_DIRECTORIES + tutor mounts. 
hooks.Filters.MOUNTED_DIRECTORIES.add_item(("openedx", r".*emi_registration$"))
