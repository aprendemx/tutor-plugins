from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()
def override_all_mfes(mfes):

    # 1) Define aquí todos tus repositorios y ramas
    custom_repos = {
        "learning": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-learning.git",
            "port": 1997,
            "version": "8bb822e342c445e39cc973435bc1647f16ae6c62",
        },
        "learner-dashboard": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-learner-dashboard.git",
            "port": 1996,
            "version": "ded563d9a3e7cf2a6a10f8c85a6216fbad156012",
        },
        "profile": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-profile.git",
            "port": 1995,
            "version": "9e59006d2547b6b1937f96ebcf96bb6100dfa19b",
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
