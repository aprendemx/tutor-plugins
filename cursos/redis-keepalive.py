# plugins/redis-keepalive.py
from tutor import hooks

# edx-platform lee CELERY_BROKER_TRANSPORT_OPTIONS del YAML de configuración
# (LMS_CFG / CMS_CFG) y lo fusiona con fanout_patterns y fanout_prefix, que se
# conservan automáticamente. Por eso el patch va en lms-env / cms-env (YAML) y
# no en *-production-settings (Python).
OPCIONES = """
CELERY_BROKER_TRANSPORT_OPTIONS:
  socket_keepalive: true
  socket_timeout: 30
  health_check_interval: 30
"""

for patch in ("lms-env", "cms-env"):
    hooks.Filters.ENV_PATCHES.add_item((patch, OPCIONES))
