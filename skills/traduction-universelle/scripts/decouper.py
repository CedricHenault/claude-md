#!/usr/bin/env python3
"""Découpe, vérifie et réassemble un long document pour la traduction.

Bibliothèque standard uniquement : aucune installation nécessaire.

Usage :
  python decouper.py decouper <source.md> --sortie <dossier_chunks> [--mots 2000]
  python decouper.py verifier <dossier_chunks> <dossier_sortie>
  python decouper.py assembler <dossier_sortie> <fichier_final.md>

Convention de nommage : chunk0001.md (source) <-> trad0001.md (traduction).
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# Caractères chinois, japonais et coréens : pas d'espaces entre les mots,
# on les compte donc à part pour estimer la longueur.
CJC = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]")
BARRIERE = re.compile(r"^\s*(```|~~~)")
TITRE = re.compile(r"^#{1,6}\s")


def mesure(texte: str) -> int:
    """Estime la longueur en « mots », y compris pour les langues sans espaces."""
    nb_cjc = len(CJC.findall(texte))
    reste = CJC.sub(" ", texte)
    return len(reste.split()) + int(nb_cjc * 0.6)


def en_blocs(texte: str) -> list[str]:
    """Sépare le texte en blocs (paragraphes) sans couper les blocs de code."""
    blocs, courant, dans_code = [], [], False
    for ligne in texte.splitlines():
        if BARRIERE.match(ligne):
            dans_code = not dans_code
        if not ligne.strip() and not dans_code:
            if courant:
                blocs.append("\n".join(courant))
                courant = []
        else:
            courant.append(ligne)
    if courant:
        blocs.append("\n".join(courant))
    return blocs


def nb_titres(texte: str) -> int:
    dans_code, n = False, 0
    for ligne in texte.splitlines():
        if BARRIERE.match(ligne):
            dans_code = not dans_code
        elif not dans_code and TITRE.match(ligne):
            n += 1
    return n


def nb_barrieres(texte: str) -> int:
    return sum(1 for ligne in texte.splitlines() if BARRIERE.match(ligne))


def empreinte(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def decouper(source: Path, sortie: Path, cible: int) -> int:
    texte = source.read_text(encoding="utf-8")
    blocs = en_blocs(texte)
    if not blocs:
        print("Erreur : le fichier source est vide.", file=sys.stderr)
        return 1

    morceaux: list[list[str]] = []
    courant: list[str] = []
    taille = 0

    def fermer():
        nonlocal courant, taille
        # Un titre ne doit pas rester seul en fin de morceau : il part avec la suite.
        reportes = []
        while len(courant) > 1 and TITRE.match(courant[-1]):
            reportes.insert(0, courant.pop())
        morceaux.append(courant)
        courant = reportes
        taille = sum(mesure(b) for b in courant)

    for bloc in blocs:
        m = mesure(bloc)
        est_titre = bool(TITRE.match(bloc))
        if courant and (
            taille + m > cible * 1.25 or (est_titre and taille >= cible * 0.6)
        ):
            fermer()
        courant.append(bloc)
        taille += m
    if courant:
        morceaux.append(courant)

    sortie.mkdir(parents=True, exist_ok=True)
    manifeste = {"source": source.name, "cible_mots": cible, "morceaux": []}
    for i, blocs_morceau in enumerate(morceaux, start=1):
        contenu = "\n\n".join(blocs_morceau) + "\n"
        nom = f"chunk{i:04d}.md"
        (sortie / nom).write_text(contenu, encoding="utf-8")
        manifeste["morceaux"].append(
            {
                "fichier": nom,
                "traduction": f"trad{i:04d}.md",
                "mots": mesure(contenu),
                "titres": nb_titres(contenu),
                "barrieres_code": nb_barrieres(contenu),
                "sha256": empreinte(contenu),
            }
        )
    (sortie / "manifest.json").write_text(
        json.dumps(manifeste, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    total = sum(m["mots"] for m in manifeste["morceaux"])
    print(f"{len(morceaux)} morceaux écrits dans {sortie} (environ {total} mots).")
    return 0


def verifier(dossier_chunks: Path, dossier_sortie: Path) -> int:
    chemin = dossier_chunks / "manifest.json"
    if not chemin.exists():
        print(f"Erreur : {chemin} introuvable.", file=sys.stderr)
        return 1
    manifeste = json.loads(chemin.read_text(encoding="utf-8"))
    erreurs, avertissements = [], []

    for m in manifeste["morceaux"]:
        src = dossier_chunks / m["fichier"]
        trad = dossier_sortie / m["traduction"]
        if not src.exists():
            erreurs.append(f"{m['fichier']} : morceau source manquant")
            continue
        texte_src = src.read_text(encoding="utf-8")
        if empreinte(texte_src) != m["sha256"]:
            avertissements.append(
                f"{m['fichier']} : la source a été modifiée depuis le découpage"
            )
        if not trad.exists():
            erreurs.append(f"{m['traduction']} : traduction manquante")
            continue
        texte_trad = trad.read_text(encoding="utf-8")
        if not texte_trad.strip():
            erreurs.append(f"{m['traduction']} : fichier vide")
            continue
        if texte_trad.strip() == texte_src.strip():
            erreurs.append(f"{m['traduction']} : identique à la source (non traduit)")
            continue
        if nb_titres(texte_trad) != nb_titres(texte_src):
            erreurs.append(
                f"{m['traduction']} : {nb_titres(texte_trad)} titres "
                f"contre {nb_titres(texte_src)} dans la source"
            )
        if nb_barrieres(texte_trad) != nb_barrieres(texte_src):
            erreurs.append(
                f"{m['traduction']} : blocs de code différents de la source"
            )
        nb_src, nb_trad = len(en_blocs(texte_src)), len(en_blocs(texte_trad))
        if nb_src and abs(nb_trad - nb_src) / nb_src > 0.2:
            avertissements.append(
                f"{m['traduction']} : {nb_trad} paragraphes contre {nb_src} "
                "dans la source, vérifier qu'aucun passage n'a été omis ou fusionné"
            )
        rapport = mesure(texte_trad) / max(mesure(texte_src), 1)
        if rapport < 0.5 or rapport > 2.0:
            avertissements.append(
                f"{m['traduction']} : longueur inhabituelle "
                f"(rapport {rapport:.2f} avec la source), à relire"
            )

    for a in avertissements:
        print(f"AVERTISSEMENT  {a}")
    for e in erreurs:
        print(f"ERREUR         {e}")
    nb = len(manifeste["morceaux"])
    if erreurs:
        print(f"\nÉchec : {len(erreurs)} erreur(s) sur {nb} morceaux.")
        return 1
    print(f"\nOK : {nb} morceaux vérifiés, {len(avertissements)} avertissement(s).")
    return 0


def assembler(dossier_sortie: Path, fichier_final: Path) -> int:
    fichiers = sorted(dossier_sortie.glob("trad[0-9][0-9][0-9][0-9].md"))
    if not fichiers:
        print(f"Erreur : aucun fichier trad*.md dans {dossier_sortie}.", file=sys.stderr)
        return 1
    parties = [f.read_text(encoding="utf-8").strip() for f in fichiers]
    fichier_final.parent.mkdir(parents=True, exist_ok=True)
    fichier_final.write_text("\n\n".join(parties) + "\n", encoding="utf-8")
    print(f"{len(fichiers)} morceaux assemblés dans {fichier_final}.")
    return 0


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sous = parseur.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("decouper", help="découper un document en morceaux")
    p.add_argument("source", type=Path)
    p.add_argument("--sortie", type=Path, required=True)
    p.add_argument("--mots", type=int, default=2000, help="taille visée par morceau")

    p = sous.add_parser("verifier", help="contrôler les traductions")
    p.add_argument("dossier_chunks", type=Path)
    p.add_argument("dossier_sortie", type=Path)

    p = sous.add_parser("assembler", help="réassembler les traductions")
    p.add_argument("dossier_sortie", type=Path)
    p.add_argument("fichier_final", type=Path)

    args = parseur.parse_args()
    if args.commande == "decouper":
        return decouper(args.source, args.sortie, args.mots)
    if args.commande == "verifier":
        return verifier(args.dossier_chunks, args.dossier_sortie)
    return assembler(args.dossier_sortie, args.fichier_final)


if __name__ == "__main__":
    sys.exit(main())
