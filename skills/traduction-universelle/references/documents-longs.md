# Documents longs et livres

Au-delà de 3 000 mots environ, deux risques apparaissent : la dérive (un terme ou un ton qui change en cours de route) et la perte (un passage sauté ou condensé sans qu'on s'en aperçoive). Cette méthode traite les deux : une fiche de style et un glossaire contre la dérive, un découpage vérifiable contre la perte.

## Vue d'ensemble

1. Préparer le texte
2. Lire et fixer les règles (glossaire et fiche de style)
3. Découper
4. Traduire morceau par morceau
5. Vérifier
6. Harmoniser
7. Reconstruire le fichier

## 1. Préparer le texte

Convertis le document en texte ou en Markdown en conservant la structure (titres, listes, notes, tableaux). Utilise l'outil disponible : un skill dédié au format (docx, pdf), `pandoc` s'il est installé, ou la lecture directe. Pour un PDF numérisé, signale que la qualité dépendra de la reconnaissance de caractères.

Dans un environnement avec fichiers, crée un dossier de travail à côté du document :

```
traduction-<nom>/
├── source.md          texte converti
├── glossaire.md       termes fixés
├── fiche-style.md     règles de style retenues
├── progression.md     état d'avancement
├── chunks/            morceaux source + manifest.json
└── sortie/            morceaux traduits
```

Ce dossier permet de reprendre un travail interrompu : au démarrage, s'il existe déjà, lis `progression.md` et continue là où le travail s'est arrêté au lieu de recommencer.

## 2. Lire et fixer les règles

Parcours l'ensemble du document avant de traduire. Pour un livre, lis au minimum l'introduction, un chapitre du milieu, la conclusion et la table des matières.

**Glossaire** : relève les termes récurrents, les noms propres, les concepts propres à l'auteur, les titres de chapitres. Fixe leur traduction. Pars du glossaire du projet (`glossaire-traduction.md`) s'il existe.

**Fiche de style**, une dizaine de lignes :

- variante de la langue cible et public visé ;
- registre, tutoiement ou vouvoiement ;
- système de temps (récit) ;
- voix de l'auteur en deux ou trois adjectifs, avec une phrase de la source qui l'illustre ;
- conventions retenues : traitement des citations, des titres d'œuvres, des unités, des notes ;
- ce qui ne se traduit pas.

Pour un texte destiné à la publication, soumets le glossaire et la fiche de style à l'utilisateur avant de traduire : une correction à ce stade coûte une ligne, après elle coûte une repasse entière.

## 3. Découper

Découpe aux frontières naturelles (chapitres, sections, puis paragraphes), jamais au milieu d'un paragraphe, en morceaux de 1 500 à 2 500 mots. Le script fourni le fait de façon déterministe et enregistre un manifeste qui servira au contrôle :

```bash
python scripts/decouper.py decouper traduction-<nom>/source.md --sortie traduction-<nom>/chunks --mots 2000
```

Sans Python, découpe à la main selon les mêmes règles et note le nombre de morceaux dans `progression.md`.

## 4. Traduire morceau par morceau

Chaque morceau se traduit avec, sous les yeux :

- le glossaire et la fiche de style ;
- les deux ou trois derniers paragraphes traduits du morceau précédent, pour la continuité du ton et des enchaînements ;
- les règles de `SKILL.md` (étapes 4 et 5) et la section utile de `types-de-contenu.md`.

Enregistre chaque traduction dans `sortie/` sous le nom `trad0001.md`, `trad0002.md`, etc., en miroir de `chunk0001.md`. Après chaque morceau, ajoute au glossaire les nouveaux termes fixés et mets à jour `progression.md`.

**Avec des sous-agents (Claude Code)** : traduis d'abord le premier morceau toi-même pour caler le ton, puis lance les suivants en parallèle. Chaque sous-agent reçoit le glossaire, la fiche de style, le premier morceau traduit comme modèle de voix, et son morceau. Demande à chacun de renvoyer aussi la liste des termes nouveaux qu'il a dû trancher : tu les fusionnes ensuite dans le glossaire et tu corriges les divergences à l'étape 6. Limite-toi à quelques sous-agents à la fois.

**Sans sous-agents, ou dans une conversation** : traduis dans l'ordre. Si le texte dépasse ce qu'une réponse peut contenir, procède par lots, indique à chaque fois « morceau X sur N » et continue au message suivant. Ne résume jamais, ne condense jamais, ne saute rien pour tenir dans la place : mieux vaut s'arrêter proprement à la fin d'un morceau et annoncer la suite.

## 5. Vérifier

```bash
python scripts/decouper.py verifier traduction-<nom>/chunks traduction-<nom>/sortie
```

Le script contrôle que chaque morceau a sa traduction, qu'elle n'est ni vide ni identique à la source, que le nombre de titres et de blocs de code correspond, et que la longueur reste plausible. Un écart de longueur est un avertissement, pas une preuve : va lire le morceau concerné.

Sans script, vérifie à la main : même nombre de morceaux, de titres, et aucun passage resté en langue source.

Retraduis tout morceau en échec. Ne le rafistole pas.

## 6. Harmoniser

Une fois tout traduit, fais une passe sur l'ensemble, centrée sur ce que la traduction par morceaux abîme :

- chaque terme du glossaire est rendu de la même façon partout (une recherche textuelle sur les variantes possibles aide) ;
- noms propres identiques d'un bout à l'autre ;
- registre et temps constants ;
- titres de chapitres cohérents avec la table des matières ;
- renvois internes (« voir chapitre 3 », « comme on l'a vu ») justes ;
- transitions entre morceaux fluides : relis chaque jointure.

Au niveau Publication, ajoute la relecture indépendante de `relecture.md`, au moins sur un échantillon : le début, la fin et deux passages du milieu. Si l'échantillon révèle des erreurs majeures, étends la relecture à tout le texte.

## 7. Reconstruire le fichier

```bash
python scripts/decouper.py assembler traduction-<nom>/sortie traduction-<nom>/<nom>.<langue>.md
```

Reconvertis ensuite dans le format d'origine avec l'outil qui a servi à l'étape 1, et contrôle la mise en page : titres, table des matières, notes, tableaux, images et légendes.

Remets à l'utilisateur le fichier final, le glossaire, et une courte liste des décisions de traduction notables. Le dossier de travail reste disponible pour des retouches.
