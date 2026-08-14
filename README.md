# Extracteur de factures

Extrait automatiquement les données de factures PDF (fournisseur, numéro,
date, montants HT/TVA/TTC) et les consolide dans un fichier CSV.

## Le problème

[2-3 phrases avec tes mots : la ressaisie manuelle, le temps que ça prend,
le risque d'erreur. C'est la section la plus importante du README.]

## Comment ça marche

1. Lecture du texte brut des PDF (pypdf)
2. Structuration via l'API Claude — gère les formats hétérogènes là où une
   regex échouerait
3. Écriture dans un CSV compatible Excel (séparateur point-virgule)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Créer un fichier `.env` à la racine :

```
ANTHROPIC_API_KEY=votre_cle
```

## Utilisation

Déposer les PDF dans `factures/`, puis lancer `python extraire.py`.

## Limites connues

- Ne traite pas les PDF scannés (pas d'OCR)
- Pas de détection de doublons
- Le parsing de la réponse casse si le modèle ajoute du texte avant le JSON
