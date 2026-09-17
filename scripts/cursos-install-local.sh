#!/usr/bin/env bash
# Instalación de la réplica local de cursos.aprende.gob.mx
#
# Cubre la sección 4.1 del documento: entorno virtual, Tutor, tema, MFE de
# autenticación y dependencias del entorno de Tutor.
#
# NO configura la instancia (cursos-config-local.sh) ni prepara la base de
# datos (cursos-db-config.py). Es idempotente: volver a ejecutarlo actualiza
# la instalación a lo que diga versions.env.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../versions.env"

BASE="${CURSOS_LOCAL:-$HOME/cursos-local}"
VENV="$BASE/venv"
PIP="$VENV/bin/pip"
TUTOR="$VENV/bin/tutor"
GH="https://github.com/aprendemx"

export TUTOR_ROOT="$BASE/tutor"
export TUTOR_PLUGINS_ROOT="$(cd "$SCRIPT_DIR/../cursos" && pwd)"

log() { printf '\n==> %s\n' "$1"; }

# Deja un repositorio en la referencia indicada, sea rama o etiqueta.
sync_repo() {
  local url="$1" dir="$2" ref="$3"
  if [ -d "$dir/.git" ]; then
    git -C "$dir" fetch --tags --prune --quiet origin
  else
    git clone --quiet "$url" "$dir"
  fi
  git -C "$dir" checkout --quiet "$ref"
  # Si la referencia es una rama, traer lo nuevo. En una etiqueta el HEAD
  # queda desprendido y el pull no aplica, de ahí el || true.
  git -C "$dir" pull --ff-only --quiet 2>/dev/null || true
}

log "Entorno virtual y Tutor $TUTOR_VERSION"
[ -d "$VENV" ] || python3 -m venv "$VENV"
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet "tutor[full]==$TUTOR_VERSION"

mkdir -p "$TUTOR_ROOT" "$BASE/src" "$BASE/mfe"

log "Tema tutor-indigo $INDIGO_TAG"
sync_repo "$GH/tutor-indigo.git" "$BASE/src/tutor-indigo" "$INDIGO_TAG"
# --no-deps: el pyproject del tema puede declarar una versión de Tutor que
# degrade la que se acaba de instalar.
( cd "$BASE/src/tutor-indigo" && "$PIP" install --quiet -e . --no-deps )

log "MFE de autenticación ($AUTHN_BRANCH)"
sync_repo "$GH/frontend-app-authn.git" "$BASE/mfe/frontend-app-authn" "$AUTHN_BRANCH"

log "Endurecimiento de seguridad en el entorno de Tutor"
"$PIP" install --quiet "git+$GH/openedx-security-hardening.git@$HARDENING_REF"

log "Montaje del MFE de autenticación"
if "$TUTOR" mounts list 2>/dev/null | grep -q "frontend-app-authn"; then
  echo "Ya estaba montado."
else
  "$TUTOR" mounts add "$BASE/mfe/frontend-app-authn"
fi

log "Resumen"
"$TUTOR" --version
"$PIP" show tutor-indigo | grep -E '^(Version|Editable)'
echo "TUTOR_ROOT=$("$TUTOR" config printroot)"
echo "TUTOR_PLUGINS_ROOT=$TUTOR_PLUGINS_ROOT"

grep -q "alias cursos=" "$HOME/.zshrc" 2>/dev/null \
  || echo "AVISO: falta el alias 'cursos' en ~/.zshrc (sección 3.1 del documento)"

cat <<EOF

Instalación lista. Pasos siguientes:

  cursos                                    # activar el entorno en tu shell
  $SCRIPT_DIR/cursos-config-local.sh        # sección 4.2
  tutor images build openedx && tutor images build mfe
  tutor local launch --non-interactive      # sección 4.4
EOF
