# chatbot-puls-events

commande d'installation des dépendances dans l'environnement virtuel :

```bash
pip install -r requirements.txt
```

commande pour build la base Faiss :

```bash
python -m builder.builder
```

commande pour lancer le bot :

```bash
streamlit run chatbot/chatbot.py
```

## Partie workflows GitHub Actions

Les workflows GitHub Actions présents dans ce dépôt sont conçus pour automatiser certaines tâches liées à la gestion des branches et aux notifications de release. Voici une brève description de chaque workflow :

1. **restrict.yml** : Ce workflow est déclenché lors de la création ou de la mise à jour d'une pull request. Il vérifie que les branches source et cible respectent un format spécifique (par exemple, `feature/`, `bugfix/`, etc.). Si le format n'est pas respecté, le workflow échoue et empêche la fusion de la pull request.
2. **notify-discord-on-release.yml** : Ce workflow est déclenché lorsqu'une nouvelle release est publiée dans le dépôt. Il envoie une notification à un canal Discord via un webhook, informant les membres de l'équipe de la nouvelle release avec des détails tels que le tag de la release et un lien vers celle-ci.
3. **notify-discord-on-push.yml** : Ce workflow est déclenché lorsqu'un push est effectué sur une branche de travail (`feature/*`, `bugfix/*`, `hotfix/*`, etc.). Il envoie une notification à un canal Discord via un webhook, informant les membres de l'équipe des nouveaux commits avec des détails tels que le message de commit et un lien vers le commit.
4. **tests-unitaires.yml** : Ce workflow est déclenché lors de la création ou de la mise à jour d'une pull request. Il exécute une série de tests unitaires pour s'assurer que les modifications apportées n'introduisent pas de régressions ou d'erreurs dans le code existant.

## Tester avec ACT 

### Tester la publication d'une release
```bash
act -e event-release.json release --secret-file .secrets
```

### Tester le push vers une branche feature
```bash
act -e event-push.json push --secret-file .secrets
```

## Configuration des secrets

Pour que les workflows de notification Discord fonctionnent correctement, vous devez configurer un secret dans votre dépôt GitHub nommé `DISCORD_WEBHOOK_URL`. Ce secret doit contenir l'URL du webhook Discord où les notifications seront envoyées.
Pour configurer un secret dans GitHub :
1. Accédez à votre dépôt GitHub.
2. Cliquez sur "Settings" (Paramètres).
3. Dans le menu de gauche, cliquez sur "Secrets and variables" puis "Actions".
4. Cliquez sur "New repository secret" (Nouveau secret de dépôt).
5. Nommez le secret `DISCORD_WEBHOOK_URL` et collez l'URL du webhook Discord dans le champ "Value" (Valeur).
6. Cliquez sur "Add secret" (Ajouter le secret) pour enregistrer.

## Regles de nommage des branches et restrictions

### Formats de branches autorisés

Les branches doivent suivre le format `type/description` avec les types suivants :

- `feature/nom-de-la-fonctionnalite` - Nouvelles fonctionnalités
- `bugfix/description-du-bug` - Corrections de bugs
- `hotfix/description-de-la-correction` - Corrections urgentes en production
- `test/description-du-test` - Tests et expérimentations
- `dev/description` - Développements divers
- `chore/description` - Tâches de maintenance
- `docs/description` - Documentation
- `refactor/description` - Refactoring de code

### Règles de merge (Pull Request obligatoire)

**Vers `main` :**
- ✅ `release/*` → `main`
- ✅ `hotfix/*` → `main`
- ❌ Aucun autre type de branche ne peut merger vers main

**Vers `development` :**
- ✅ `feature/*` → `development`
- ✅ `bugfix/*` → `development`
- ✅ `dev/*`, `test/*`, `chore/*`, `docs/*`, `refactor/*` → `development`
- ❌ Les branches `release/*` et `hotfix/*` ne peuvent pas merger vers development

**Vers `release/*` :**
- ✅ `bugfix/*` → `release/*` (corrections uniquement)
- ❌ Aucun autre type de branche ne peut merger vers release

### Protection des branches principales

⚠️ **Les pushs directs sont interdits** sur `main`, `development` et `release/*`. Utilisez toujours une Pull Request depuis une branche de travail.

Le workflow `restrict.yml` valide automatiquement ces règles lors de chaque Pull Request.

