# TriageBot

TriageBot analyse des tickets de support avec un modèle de langage exécuté par [Ollama](https://ollama.com/). Il attribue à chaque ticket une catégorie, une sévérité, un sentiment et un résumé, puis enregistre les résultats et affiche un tableau de bord dans le terminal.

## Prérequis

- Python 3.13 ou ultérieur
- Ollama installé et démarré ([téléchargement officiel](https://ollama.com/download))
- Le modèle Ollama `llama3.1:8b` (plusieurs gigaoctets à télécharger)

## Installation

Les commandes ci-dessous sont à exécuter depuis le dossier racine du projet, celui qui contient `requirements.txt`.

### Linux et macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Si PowerShell bloque l’activation de l’environnement virtuel, ouvrez une nouvelle fenêtre PowerShell ou suivez la documentation Microsoft sur les stratégies d’exécution PowerShell. Vous pouvez aussi lancer directement `.\.venv\Scripts\python.exe` à la place de `python` dans les commandes suivantes.

Téléchargez ensuite le modèle requis :

```bash
ollama pull llama3.1:8b
```

Ollama doit rester démarré pendant l’analyse. S’il ne l’est pas déjà, lancez `ollama serve` dans un autre terminal et laissez ce terminal ouvert. Si la commande indique qu’un serveur est déjà actif, ne lancez pas une seconde instance.

## Lancer le triage

Après avoir activé l’environnement virtuel, depuis la racine du projet :

```bash
python src/main.py
```

Sous Windows, si l’environnement virtuel n’est pas activé :

```powershell
.\.venv\Scripts\python.exe src\main.py
```

Le programme lit `data/tickets.json`, ignore les tickets dont le message est vide ou composé d’espaces, et élimine les doublons ayant le même joueur et le même message. Les tickets conservés sont analysés un par un. Le tableau de bord s’affiche dans le terminal à la fin.

## Format des tickets

`data/tickets.json` doit contenir un tableau JSON. Chaque élément doit avoir un identifiant, un joueur et un message :

```json
[
  {
    "id": 1,
    "player": "NomDuJoueur",
    "message": "Le jeu plante quand j'ouvre mon inventaire."
  }
]
```

Vous pouvez modifier ce fichier pour traiter vos propres tickets. Veillez à conserver un JSON valide et les trois champs attendus.

## Résultats

Les résultats sont enregistrés dans `output/results.json`. À chaque lancement, ce fichier est remplacé par les résultats de l’analyse en cours. Chaque résultat contient le ticket initial et son analyse (`categorie`, `severite`, `sentiment` et `resume`). Le document comprend également la date de mise à jour et le nombre de tickets traités.

Si Ollama est indisponible ou si l’analyse d’un ticket échoue, le ticket est marqué avec le statut `to_check` dans le fichier de résultats. Vérifiez alors qu’Ollama est démarré et que le modèle `llama3.1:8b` est installé, puis relancez le programme.

## Catégories

Le modèle est invité à classer les tickets dans l’une des catégories suivantes : `bug`, `payment`, `account`, `suggestion`, `toxicity` ou `autre`.

La sévérité va de 1 (faible) à 5 (critique).

## Bonus sécurité : détection des injections de prompt

Avant d’envoyer un message à Ollama, le bot recherche sans tenir compte de la casse des expressions typiques d’une tentative de manipulation, par exemple `ignore`, `instructions précédentes`, `system override` ou `tu es maintenant`. Si une expression est détectée, le ticket est bloqué avant l’appel au modèle et reçoit directement la catégorie `toxicity`, la sévérité 1 et le résumé `[BLOQUÉ] Tentative d’injection de prompt.`

Cette parade évite de laisser le modèle suivre les instructions contenues dans les tickets repérés. Elle repose toutefois sur une liste de mots-clés : elle peut manquer une formulation inconnue ou signaler à tort un message légitime. Ce filtre est une première défense, pas une garantie de sécurité complète.
