from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()
def override_all_mfes(mfes):

    # 1) Define aquí todos tus repositorios y ramas
    custom_repos = {
        "profile": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-profile.git",
            "port": 1995,
            "version": "072caaf3fb3d551e45e8392ff00555e5d602cb56",
        },
        "authn":{
            "repository": "https://github.com/aprendemx/emi-frontend-app-authn.git",
            "port": 2000,
            "version": "dc25af3db0f854253e1340f23f8f99dce943caf8",
        },
    }


    # 2) Recorre y reemplaza cada entrada en mfes
    for name, cfg in custom_repos.items():
        # Elimina la definición original (si existiera)
        mfes.pop(name, None)
        # Añade tu fork bajo la misma clave
        mfes[name] = {
            "repository": cfg["repository"],
            "port": cfg["port"],
            "version": cfg["version"],
        }

    return mfes
