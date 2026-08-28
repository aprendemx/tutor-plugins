"""
emi-db-config.py — configuracion de EMI que vive en la base de datos.

Waffle flags, switches y SiteConfiguration no se guardan en config.yml ni en
ningun repositorio: viven en MySQL. Si la instancia se reconstruye desde cero,
se pierden y la plataforma arranca sirviendo plantillas Mako en vez de los MFEs
(entre ellas dashboard.html, que ademas esta rota).

USO
---
Desde la raiz de Tutor, con el entorno correcto cargado:

    tutor local exec lms bash -c 'cd /openedx/edx-platform && ./manage.py lms shell' \\
      < scripts/emi-db-config.py

Es idempotente: se puede ejecutar tantas veces como haga falta.

Se intento registrarlo como tarea de inicializacion con el filtro
CLI_DO_INIT_TASKS, pero en Tutor 20.0.1 ese filtro no surte efecto desde un
plugin de un solo archivo (verificado con un plugin de prueba minimo). Por eso
es un script manual y no automatico.

IMPORTANTE: ejecutar despues de cada `tutor local launch` sobre una base de
datos nueva, y despues de cualquier reconstruccion de la instancia.
"""

from django.contrib.sites.models import Site
from django.conf import settings
from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from waffle.models import Flag, Switch

# --- Waffle flags: activan los MFEs. Sin ellas se sirven plantillas Mako. ---
FLAGS = [
    "learner_profile.redirect_to_microfrontend",
    "learner_home_mfe.enabled",
    "course_home.course_home_mfe_progress_tab",
    "new_studio_mfe.use_new_home_page",
    "discussions.enable_learners_tab_in_discussions_mfe",
    "discussions.enable_learners_stats",
]

SWITCHES = [
    "completion.enable_completion_tracking",
]

# Debe coincidir con EXTRA_KEYS de emi_registration/forms.py.
# Sin esta lista, los campos extra del registro no se guardan.
EXTENDED_PROFILE_FIELDS = [
    "first_lastname",
    "second_lastname",
    "municipality",
    "school_name",
    "grade",
    "cct",
    "curp",
]

SITE_VALUES = {
    "ENABLE_PROFILE_MICROFRONTEND": "true",
    "extended_profile_fields": EXTENDED_PROFILE_FIELDS,
}


def dominios():
    """Deriva los dominios del LMS_BASE, para que sirva en EMI y en local."""
    base = settings.LMS_BASE.split(":")[0]
    return [base, f"{base}:8000"]


print("=== emi-db-config ===")

for nombre in FLAGS:
    flag, creada = Flag.objects.get_or_create(name=nombre)
    if not flag.everyone:
        flag.everyone = True
        flag.save()
        estado = "creada" if creada else "activada"
    else:
        estado = "ya estaba"
    print(f"  flag    {nombre}: {estado}")

for nombre in SWITCHES:
    switch, creado = Switch.objects.get_or_create(name=nombre)
    if not switch.active:
        switch.active = True
        switch.save()
        estado = "creado" if creado else "activado"
    else:
        estado = "ya estaba"
    print(f"  switch  {nombre}: {estado}")

for dominio in dominios():
    site, _ = Site.objects.get_or_create(domain=dominio, defaults={"name": dominio})
    config, creada = SiteConfiguration.objects.get_or_create(
        site=site, defaults={"site_values": SITE_VALUES, "enabled": True}
    )
    if not creada:
        # Fusiona en vez de sobrescribir: puede haber claves puestas a mano
        # que no queremos perder.
        valores = dict(config.site_values or {})
        valores.update(SITE_VALUES)
        config.site_values = valores
        config.enabled = True
        config.save()
    print(f"  site    {dominio}: {'creada' if creada else 'actualizada'}")

print("=== listo ===")
