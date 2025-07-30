# Arcane Secret Manager

Ce package est basé sur [google-cloud-secret-manager](https://pypi.org/project/google-cloud-secret-manager/).

## Installation

```sh
pip install arcane-secretmanager
```

## Utilisation

### Initialisation avec clé de service

```python
from arcane import secretmanager

# Avec un fichier de clé de service
client = secretmanager.Client('/path/to/service-account-key.json')

# Ou avec les credentials par défaut
client = secretmanager.Client()
```

### Récupérer un secret

```python
# Récupérer la dernière version d'un secret
value = client.get_secret_value('my-project', 'my-secret')

# Récupérer une version spécifique
value = client.get_secret_value('my-project', 'my-secret', '2')
```

### Créer un secret

```python
# Créer un nouveau secret
secret_name = client.create_new_secret('my-project', 'my-secret')

# Créer un secret avec des labels
secret_name = client.create_new_secret(
    'my-project', 
    'my-secret',
    labels={'env': 'production', 'team': 'backend'}
)
```

### Ajouter une version

```python
# Ajouter une nouvelle version à un secret existant
version_name = client.add_new_secret_version('my-project', 'my-secret', 'my-secret-value')
```

### Lister les secrets

```python
# Lister tous les secrets d'un projet
secrets = client.get_all_secrets('my-project')
for secret in secrets:
    print(f"Secret: {secret['name']}")
```

### Supprimer un secret

```python
# Supprimer un secret
client.remove_secret('my-project', 'my-secret')
```

### Mettre à jour les labels

```python
# Mettre à jour les labels d'un secret
client.update_secret_labels('my-project', 'my-secret', {'env': 'staging'})
```
