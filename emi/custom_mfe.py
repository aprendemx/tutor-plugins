from tutormfe.hooks import MFE_APPS

@MFE_APPS.add()
def override_all_mfes(mfes):

    # 1) Define aquí todos tus repositorios y ramas
    custom_repos = {
        "learner-dashboard": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-learner-dashboard.git",
            "port": 1996,
            "version": "370434e7ba2a3c443fa725faf63d7e43cf7d54f5",
        },
        "profile": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-profile.git",
            "port": 1995,
            "version": "b189131e87a4b81ef7fe0e2fcc613a45ef2caf97",
        },
        "learning": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-learning.git",
            "port": 1997,
            "version": "307e41b88a70bddd8633f9152b9c915613a2499b",
        },
        "account": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-account.git",
            "port": 1998,
            "version": "4e5b5c8a18f05e4222839df587c235dc8e8d0a78",
        },
	    "discussions": {
            "repository": "https://github.com/aprendemx/emi-frontend-app-discussions.git",
            "port": 1999,
            "version": "1b9f8dcbcb3457aa91cc381167576ab9bba1bafd",
	    },
        "authn":{
            "repository": "https://github.com/aprendemx/emi-frontend-app-authn.git",
            "port": 2000,
            "version": "4e14c2c779dbb1a8f18792be2d8461536f2a2023",
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
