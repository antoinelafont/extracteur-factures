import json
import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic
from pypdf import PdfReader

load_dotenv()
client = Anthropic()

DOSSIER = Path("factures")

PROMPT = """Voici le texte brut extrait d'une facture PDF. L'ordre des éléments est désordonné.

Renvoie UNIQUEMENT un objet JSON, sans texte autour, sans balises markdown, avec ces clés :
- fournisseur (string)
- numero_facture (string)
- date_emission (string, format AAAA-MM-JJ)
- total_ht (number)
- tva (number)
- total_ttc (number)

Si une information est absente, mets null.

Texte de la facture :
"""


def extraire_texte(chemin_pdf):
    reader = PdfReader(chemin_pdf)
    texte = ""
    for page in reader.pages:
        texte += page.extract_text() or ""
    return texte


def analyser(texte):
    reponse = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{"role": "user", "content": PROMPT + texte}],
    )
    brut = reponse.content[0].text.strip()

    if brut.startswith("```"):
        lignes = brut.split("\n")
        brut = "\n".join(lignes[1:-1])

    return json.loads(brut)


COLONNES = [
    "fichier",
    "fournisseur",
    "numero_facture",
    "date_emission",
    "total_ht",
    "tva",
    "total_ttc",
]

lignes = []

for fichier in DOSSIER.glob("*.pdf"):
    print(f"Traitement de {fichier.name}...")
    texte = extraire_texte(fichier)
    donnees = analyser(texte)
    donnees["fichier"] = fichier.name
    lignes.append(donnees)

with open("resultat.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=COLONNES, delimiter=";")
    writer.writeheader()
    writer.writerows(lignes)

print(f"{len(lignes)} factures écrites dans resultat.csv")