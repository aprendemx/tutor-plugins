#!/usr/bin/env bash
# Configuración de la réplica local de cursos.aprende.gob.mx
set -euo pipefail

source "$(dirname "$0")/../versions.env"

GH=https://github.com/aprendemx
EXTRA_PIP=$(cat <<EOF
["git+https://github.com/open-craft/xblock-poll.git@${XBLOCK_POLL_REF}",
 "git+${GH}/Edx-Oauth2.git@${EDX_OAUTH2_REF}",
 "git+${GH}/custom-registration-form.git@${CUSTOM_REG_FORM_REF}",
 "git+${GH}/llavemx_mobile_bridge.git@${LLAVEMX_BRIDGE_REF}",
 "git+${GH}/openedx-security-hardening.git@${HARDENING_REF}",
 "git+${GH}/openedx-sso-gateway.git@${SSO_GATEWAY_REF}",
 "git+${GH}/aprende-openedx-customizations.git@${APRENDE_CUSTOMIZATIONS_REF}"]
EOF
)
EXTRA_PIP=$(echo "$EXTRA_PIP" | tr -d '\n ')

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
  --set OPENEDX_EXTRA_PIP_REQUIREMENTS="$EXTRA_PIP"

tutor plugins enable admin_password_reset aprende_customizations custom_reg_form \
  delete_account enable_bulk_email forum google_analytics gradebook indigo \
  llavemx_mobile_bridge logos mfe minio rate_limit redis-keepalive \
  security_hardening set_default_enrollment sso-gataway unenroll worker-concurrency

tutor config save 2>&1 | grep -iE "warn|fail|error" || true
