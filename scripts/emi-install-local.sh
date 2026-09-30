#!/usr/bin/env bash
# Instalación de la réplica local de emi.aprende.gob.mx
#
# Cubre la sección 4.1 del documento: entorno virtual, Tutor y tema.
#
# NO configura la instancia (emi-config-local.sh) ni prepara la base de
# datos (emi-db-config.py). Es idempotente: volver a ejecutarlo actualiza
# la instalación a lo que diga versions.env.
#
# A diferencia de cursos, aquí no se clona ni se monta ningún MFE: EMI
# construye los seis forks desde custom_mfe.py, que ya los fija por commit.
# El montaje es solo para iterar (sección 6.2 del documento).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/../versions.env"

BASE="${EMI_LOCAL:-$HOME/emi-local}"
VENV="$BASE/venv"
PIP="$VENV/bin/pip"
TUTOR="$VENV/bin/tutor"
GH="https://github.com/aprendemx"

export TUTOR_ROOT="$BASE/tutor"
export TUTOR_PLUGINS_ROOT="$(cd "$SCRIPT_DIR/../emi" && pwd)"

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

log "Entorno virtual y Tutor $EMI_TUTOR_VERSION"
[ -d "$VENV" ] || python3 -m venv "$VENV"
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet "tutor[full]==$EMI_TUTOR_VERSION"

mkdir -p "$TUTOR_ROOT" "$BASE/src"

log "Tema emi ($EMI_THEME_REF)"
sync_repo "$GH/emi-theme.git" "$BASE/src/emi-theme" "$EMI_THEME_REF"
# --no-deps: el pyproject del tema puede declarar una versión de Tutor que
# degrade la que se acaba de instalar.
( cd "$BASE/src/emi-theme" && "$PIP" install --quiet -e . --no-deps )

log "Resumen"
"$TUTOR" --version
"$PIP" show emi | grep -E '^(Version|Editable)'
echo "TUTOR_ROOT=$("$TUTOR" config printroot)"
echo "TUTOR_PLUGINS_ROOT=$TUTOR_PLUGINS_ROOT"

grep -q "alias emi=" "$HOME/.zshrc" 2>/dev/null \
  || echo "AVISO: falta el alias 'emi' en ~/.zshrc (sección 3.1 del documento)"

cat <<EOF

Instalación lista. Pasos siguientes:

  emi                                    # activar el entorno en tu shell
  $SCRIPT_DIR/emi-config-local.sh        # sección 4.2
  tutor images build openedx && tutor images build mfe
  tutor local launch --non-interactive   # sección 4.4
EOF
