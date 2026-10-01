import os
from tutor import hooks

# EMI: estilos para MFEs que usan upstream sin fork (account y discussions).
# Antes de compilar, el patch escribe src/_emi.scss y lo importa al final de
# src/index.scss, para que sus reglas ganen a las de upstream. Los estilos
# viven como .scss en mfe-estilos/.
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mfe-estilos")

def leer(nombre):
    with open(os.path.join(DIR, nombre), encoding="utf-8") as f:
        return f.read()

for app in ["account", "discussions"]:
    css = leer("encabezado.scss") + "\n" + leer(app + ".scss")
    patch = (
        'COPY <<"EMI_EOF" /openedx/app/src/_emi.scss\n' + css + "\nEMI_EOF\n"
        + "RUN printf '\\n@import \"./emi\";\\n' >> /openedx/app/src/index.scss\n"
    )
    hooks.Filters.ENV_PATCHES.add_item(("mfe-dockerfile-pre-npm-build-" + app, patch))
