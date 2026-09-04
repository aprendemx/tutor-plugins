"""
cursos-db-config.py — estado que solo vive en la base de datos.

Réplica local de cursos.aprende.gob.mx. Idempotente: se puede correr N veces.

    docker exec -i tutor_local-lms-1 \
        bash -c 'cd /openedx/edx-platform && ./manage.py lms shell' \
        < cursos-db-config.py
"""

LMS_DOMAIN = "local.openedx.io"
SITE_ID_PROD = 18          # el que fija site.py en producción
THEME = "indigo"

# ---------------------------------------------------------------- sites
from django.contrib.sites.models import Site
from openedx.core.djangoapps.theming.models import SiteTheme
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration

# Site.domain es unique: el site autogenerado por Tutor ocupa el dominio que
# necesitamos para el id 18. Se borra (arrastra su theme y su config) y se
# recrea con el id correcto.
borrados = Site.objects.filter(domain=LMS_DOMAIN).exclude(id=SITE_ID_PROD).delete()
print("SITES BORRADOS:", borrados)

site, creado = Site.objects.update_or_create(
    id=SITE_ID_PROD,
    defaults={"domain": LMS_DOMAIN, "name": LMS_DOMAIN},
)
print("SITE", site.id, site.domain, "creado" if creado else "actualizado")

# Sin esto los correos salen con la plantilla del core: Celery los manda sin
# petición HTTP, así que el tema se resuelve por SITE_ID.
theme, _ = SiteTheme.objects.update_or_create(
    site=site, defaults={"theme_dir_name": THEME}
)
print("THEME", theme.site_id, "->", theme.theme_dir_name)

conf, _ = SiteConfiguration.objects.update_or_create(
    site=site,
    defaults={
        "enabled": True,
        "site_values": {
            "ENABLE_PROFILE_MICROFRONTEND": "true",
            "LANGUAGE_CODE": "es-419",
            "ALWAYS_REDIRECT_HOMEPAGE_TO_DASHBOARD_FOR_AUTHENTICATED_USER": False,
        },
    },
)
print("SITECONFIG", conf.site_id, sorted(conf.site_values.keys()))

Site.objects.clear_cache()

# ---------------------------------------------------------------- waffle
# De las 24 diferencias contra producción, 23 son flags de versiones
# anteriores que Ulmo ya no consulta. La única viva es este switch, y es
# el que hace que las constancias se emitan solas.
from waffle.models import Switch

sw, _ = Switch.objects.update_or_create(
    name="certificates.auto_certificate_generation", defaults={"active": True}
)
print("SWITCH", sw.name, sw.active)

# ---------------------------------------------------------- organizaciones
# Muestra mínima para probar los logos de las constancias, no las 54.
from organizations.models import Organization

ORGS = [
    ("aprendemx", "Dirección General @prende.mx"),
    ("UnADM", "Universidad Abierta y a Distancia de México"),
    ("MexicoX", "mexicox.gob.mx"),
    ("CENAPRED", "Centro Nacional de Prevención de Desastres"),
    ("SNDIF", "Sistema Nacional para el Desarrollo Integral de la Familia"),
]
for short_name, name in ORGS:
    org, creado = Organization.objects.update_or_create(
        short_name=short_name, defaults={"name": name, "active": True}
    )
    print("ORG", org.short_name, "creada" if creado else "ok")

print("LISTO. Los logos se suben a mano desde el admin de organizaciones.")
