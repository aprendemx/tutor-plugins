# tutor-plugins

Plugins de Tutor de las instancias de Open edX de @prende.mx.

No se instalan con pip: son archivos que se copian a la raíz de plugins de
cada servidor y se habilitan con `tutor plugins enable <nombre>`.

La ruta varía por instancia — consultar con `tutor plugins printroot`:
- producción / cursos-dev: `/opt/tutor/plugins/`
- EMI: `/opt/tutor-plugins/`

**`installed` no es `enabled`.** Un `.py` en esa ruta se autodescubre pero no
se activa. Sin el `enable`, sus `ENV_PATCHES` nunca se registran y no hay
ningún error.

## emi/

| Plugin | Estado | Qué hace |
|---|---|---|
| `campos_extras.py` | enabled | Campos extra de registro (CURP, escuela, CCT, grado). Declara `REGISTRATION_EXTRA_FIELDS`, `REGISTRATION_EXTENSION_FORM`, el mount de `emi_registration` y su alta en `INSTALLED_APPS` |
| `custom_mfe.py` | enabled | Sustituye 6 MFEs por los forks institucionales vía `MFE_APPS`, pineados a SHA |
| `google_analytics.py` | enabled | `GOOGLE_ANALYTICS_4_ID` en LMS y MFEs |

### emi/retirados/

| Plugin | Por qué |
|---|---|
| `corsplugin.py` | Configuración de desarrollo con IP pública hardcodeada. **Asigna** `CORS_ORIGIN_WHITELIST` en lugar de extenderla: habilitarlo borraría los orígenes existentes. Usa el patch `lms-env`, aparentemente obsoleto |

## Verificar tras editar un plugin

Un error de sintaxis **no detiene** `tutor config save`: emite una advertencia
de una línea y sigue, dejando el `env/` sin las personalizaciones del plugin.

```bash
python3 -c "import ast; ast.parse(open('<plugin>.py').read())" && echo OK
tutor plugins list | grep <plugin>          # debe decir 'enabled'
tutor config save
sudo diff -r <respaldo>/env-antes /opt/tutor/env
```

Un diff mucho mayor de lo previsto casi siempre significa que un plugin dejó
de cargar.
