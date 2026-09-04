#!/usr/bin/env bash
# Configuración de la réplica local de cursos.aprende.gob.mx
set -euo pipefail

tutor config save \
  --set LMS_HOST=local.openedx.io \
  --set CMS_HOST=studio.local.openedx.io \
  --set PLATFORM_NAME="Cursos aprendeMX local" \
  --set LANGUAGE_CODE=es-mx \
  --set OPENEDX_LMS_UWSGI_WORKERS=2 \
  --set OPENEDX_CMS_UWSGI_WORKERS=2 \
  --set CONTACT_EMAIL=cursos@aprende.gob.mx \
  --set INFO_EMAIL=contacto@aprende.gob.mx \
  --set ACTIVATION_EMAIL_SUPPORT_LINK=https://soporte.aprende.gob.mx \
  --set INDIGO_ENABLE_DARK_TOGGLE=false \
  --set OPENEDX_EXTRA_PIP_REQUIREMENTS='["git+https://github.com/open-craft/xblock-poll.git@d2459e7bdf52fcb2b400684627bdcbd2e9302598","git+https://github.com/aprendemx/Edx-Oauth2.git@f4c735ce8aa549d64a0619b4155fec3c40318e63","git+https://github.com/aprendemx/custom-registration-form.git@0.1.8","git+https://github.com/aprendemx/llavemx_mobile_bridge.git@f100f336e0b04cd1e8ea8e520c78600ac835bd54","git+https://github.com/aprendemx/openedx-security-hardening.git@a2669e123e7c524c0679f75b759d9fa42b2d9479","git+https://github.com/aprendemx/openedx-sso-gateway.git@9b8ddff4353e85829e09844caa29b2e74acabb19","git+https://github.com/aprendemx/aprende-openedx-customizations.git@45ecd460e693c28b21f8034e8bae407a1a9e409f"]'

tutor plugins enable admin_password_reset aprende_customizations custom_reg_form \
  delete_account enable_bulk_email forum google_analytics gradebook indigo \
  llavemx_mobile_bridge logos mfe minio rate_limit redis-keepalive \
  security_hardening set_default_enrollment sso-gataway unenroll worker-concurrency

tutor config save 2>&1 | grep -iE "warn|fail|error" || true
