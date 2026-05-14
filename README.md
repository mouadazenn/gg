# Ventec KPI Dashboard — Streamlit

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

Ouvre ensuite http://localhost:8501 dans ton navigateur.

## Comptes de démo

| Nom            | Email                 | Mot de passe | Rôle    |
|----------------|-----------------------|--------------|---------|
| Administrateur | admin@ventec.ma       | admin123     | Admin   |
| Manager QSE    | manager@ventec.ma     | manager123   | Manager |
| Lecteur        | viewer@ventec.ma      | viewer123    | Lecteur |

## Rôles et permissions

- **Admin** : accès complet (dashboard, saisie, rapport, gestion utilisateurs)
- **Manager** : accès dashboard, saisie et rapport (pas gestion utilisateurs)
- **Lecteur** : dashboard et rapport en lecture seule (pas de saisie)

## Structure des fichiers

```
ventec_dashboard/
├── app.py          # Application principale Streamlit
├── data.py         # KPIs, macro-processus, utilisateurs, génération de données
└── requirements.txt
```

## Ajouter un vrai utilisateur

Dans `data.py`, modifier la liste `USERS` :

```python
USERS = [
    {'id': 1, 'n': 'Prénom Nom', 'e': 'email@ventec.ma', 'p': 'motdepasse', 'ro': 'admin', 'a': True},
    ...
]
```

Pour une production réelle, utilise `st.secrets` ou une base de données pour stocker les mots de passe de manière sécurisée (avec hachage bcrypt par exemple).
