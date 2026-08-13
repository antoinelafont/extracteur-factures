from pathlib import Path
from pypdf import PdfReader

DOSSIER = Path("factures")

def extraire_texte(chemin_pdf):
    reader = PdfReader(chemin_pdf)
    texte = ""
    for page in reader.pages:
        texte += page.extract_text() or ""
    return texte 

for fichier in DOSSIER.glob("*.pdf"):
    print(f"--- {fichier.name} ---")
    print(extraire_texte(fichier)[:500])
    print()