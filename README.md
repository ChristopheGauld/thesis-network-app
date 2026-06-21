# Sémiologie et réseaux

Application Streamlit sombre et interactive présentant les résultats principaux de la thèse de Christophe Gauld sur les applications cliniques et neuroscientifiques des réseaux de symptômes.

## Contenu

- synthèse des quatre études empiriques ;
- résultats méthodologiques et limites d’interprétation ;
- résultats cliniques et figures principales ;
- onglet dédié au modèle dynamique couplé x–y–z–f ;
- simulation paramétrable des quatre équations discutées dans *Dynamical Systems for Computational Psychiatry* et espaces de phase.

Le manuscrit et les données individuelles ne sont pas inclus dans le dépôt.

## Lancer localement

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Déployer

Le dépôt est compatible avec Streamlit Community Cloud. Choisir `app.py` comme fichier principal. Pour un dépôt privé, vérifier que l’espace Streamlit utilisé dispose d’un accès GitHub approprié.

## Données

L’application fonctionne sans données brutes. Des données anonymisées permettraient d’ajouter des filtres de sous-groupes, des réseaux recalculés, des trajectoires individuelles et des analyses de sensibilité. Ne jamais déposer de données directement identifiantes ou ré-identifiables.

## Avertissement

La simulation du système X–Y–Z est une illustration pédagogique du cadre formel de la thèse. Elle n’est pas ajustée aux données empiriques et ne constitue pas un outil de décision clinique.
