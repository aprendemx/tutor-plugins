#!/usr/bin/env bash
# Configuración de la réplica local de emi.aprende.gob.mx
set -euo pipefail

source "$(dirname "$0")/../versions.env"

GH=https://github.com/aprendemx
EXTRA_PIP=$(cat <<EOF
["git+${GH}/emi-customizations.git@${EMI_CUSTOMIZATIONS_REF}",
 "git+${GH}/emi-registration.git@${EMI_REGISTRATION_REF}"]
EOF
)
EXTRA_PIP=$(echo "$EXTRA_PIP" | tr -d '\n ')

# LANGUAGE_CODE se queda en 'en' por fidelidad: es lo que corre la MV, aunque
# la plataforma se use en español. Cambiarlo aquí ocultaría diferencias reales.
#
# RUN_MYSQL y RUN_SMTP van explícitos aunque el valor por defecto ya sea true:
# en la MV son false (MySQL en 10.1.1.10, correo por SendGrid) y conviene que
# el script deje constancia de que en local todo es autocontenido.
tutor config save \
  --set LMS_HOST=local.openedx.io \
  --set CMS_HOST=studio.local.openedx.io \
  --set PLATFORM_NAME="EMI local" \
  --set LANGUAGE_CODE=en \
  --set RUN_MYSQL=true \
  --set RUN_SMTP=true \
  --set OPENEDX_LMS_UWSGI_WORKERS=2 \
  --set OPENEDX_CMS_UWSGI_WORKERS=2 \
  --set LMS_ROOT_URLCONF=emi.urls \
  --set INDIGO_ENABLE_DARK_TOGGLE=false \
  --set OPENEDX_EXTRA_PIP_REQUIREMENTS="$EXTRA_PIP" \
  --set ATLAS_REPOSITORY="$EMI_ATLAS_REPOSITORY" \
  --set ATLAS_REVISION="$EMI_ATLAS_REVISION"

tutor plugins enable campos_extras custom_mfe delete_account emi mfe_estilos forum google_analytics \
  indigo mfe minio set_default_enrollment

tutor config save 2>&1 | grep -iE "warn|fail|error" || true

# Comprobaciones antes de invertir 40 minutos en construir.
echo
echo "== Verificación =="
tutor config printvalue LMS_HOST
tutor config printvalue LMS_ROOT_URLCONF
echo -n "plugins habilitados: "; tutor plugins list | grep -c enabled   # 9
echo -n "dependencias git en el Dockerfile: "
grep -c "git+https" "$(tutor config printroot)/env/build/openedx/Dockerfile"   # 2
echo -n "MFEs propios en MFE_CONFIG: "
grep -c "emi-frontend-app" "$(tutor config printroot)/env/build/mfe/Dockerfile" || true

cat <<'EOF'

PENDIENTE DE CONFIRMAR CONTRA LA MV
  Las traducciones propias (aprendemx/emi-openedx-translations, rama
  chore/teak-translation) entran por ATLAS_REPOSITORY/ATLAS_REVISION. Falta
  verificar si en EMI se pasan como --build-arg o desde config.yml, y añadir
  aquí la línea correspondiente.

  MFE_CONFIG.ENABLE_DYNAMIC_REGISTRATION_FIELDS debe quedar en true para que
  se vean los campos adicionales del registro. Si no lo fija campos_extras.py,
  hay que añadirlo con un patch de plugin, no con --set.
EOF
