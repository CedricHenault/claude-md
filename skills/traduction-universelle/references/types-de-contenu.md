# Règles par type de contenu

Lis uniquement la section qui correspond au texte à traduire.

## Sommaire

1. Littéraire (roman, nouvelle, essai)
2. Poésie et chansons
3. Documentation technique
4. Chaînes d'interface et logiciel
5. Données structurées (JSON, YAML, CSV, XML)
6. Juridique et administratif
7. Marketing et publicité
8. Sous-titres
9. Académique et scientifique
10. Médical
11. Correspondance
12. Presse et web

---

## 1. Littéraire (roman, nouvelle, essai)

L'objet à restituer est une voix. La justesse du sens ne suffit pas : le rythme, la longueur des phrases, les répétitions voulues, le niveau de langue de chaque personnage font partie du texte.

- Repère avant de commencer la voix du narrateur et celle de chaque personnage, et tiens-les.
- Choisis le système de temps du récit selon la langue cible et garde-le. En français, un récit au prétérit anglais se rend selon le ton par le passé simple (récit classique) ou le passé composé (récit oral, contemporain) ; décide une fois, puis ne varie plus.
- Applique les conventions de dialogue de la langue cible : tirets cadratins en français et en espagnol, guillemets en anglais, 「」 en japonais.
- Garde les répétitions et les figures de style voulues. Ne « corrige » pas un style.
- Références culturelles : conserve-les. N'ajoute une précision que si le lecteur cible est perdu sans elle, et le plus discrètement possible. Pas de note de bas de page sans demande.
- Noms de personnages et de lieux : ne les traduis pas, sauf s'ils sont porteurs de sens et que la tradition du genre le veut (fantasy, jeunesse). Dans ce cas, décide une fois et inscris le choix au glossaire.
- Jeux de mots : cherche un jeu équivalent en langue cible, quitte à s'éloigner de la lettre. Si rien ne fonctionne, rends le sens et signale la perte en note.
- Essai et non-fiction d'auteur : le raisonnement doit rester aussi serré que dans l'original. Garde les connecteurs logiques et la progression des arguments ; ne lisse pas les formules marquantes.

## 2. Poésie et chansons

On ne peut pas tout conserver à la fois : sens, rimes, mètre, sonorités. Annonce en une ligne ce que tu privilégies, ou demande si l'usage n'est pas clair.

- Pour comprendre le texte : privilégie le sens, en vers libres, en gardant les images et les coupes.
- Pour être dit ou chanté : privilégie le mètre et la rime, et accepte de t'éloigner de la lettre. Vérifie le nombre de syllabes.
- Propose volontiers une version littérale à côté de la version travaillée.

## 3. Documentation technique

Le lecteur veut exécuter une tâche sans se tromper. Clarté et exactitude passent avant l'élégance.

- Ne traduis jamais le code, les commandes, les noms de fichiers, de fonctions, de paramètres, ni les sorties de terminal. Les commentaires dans le code se traduisent si la documentation entière est traduite.
- Libellés d'interface cités dans le texte (boutons, menus) : utilise le libellé réel de la version localisée du produit si tu le connais. Sinon, garde l'original suivi de la traduction entre parenthèses à la première occurrence.
- Terminologie : suis celle qui est établie dans le domaine pour la langue cible. Un terme anglais couramment gardé tel quel par les praticiens (par exemple « commit », « pull request ») reste en anglais.
- Phrases courtes, mode impératif ou infinitif selon la convention de la langue cible pour les procédures (en français : infinitif ou impératif, choisis et tiens).
- Garde la numérotation des étapes, les avertissements, les renvois et les ancres de liens intacts.

## 4. Chaînes d'interface et logiciel

Chaque chaîne s'affiche seule, hors contexte, dans un espace limité.

- Garde intactes les variables et balises : `{name}`, `%s`, `%1$d`, `{{count}}`, `<b>`, `\n`. Déplace-les selon la grammaire cible sans les modifier.
- Concision : vise une longueur proche de la source. Signale les chaînes nettement plus longues, qui risquent de déborder.
- Pluriels : la langue cible peut avoir plus de formes que la source (russe, arabe, polonais). Si le format le permet (ICU, gettext), fournis toutes les formes requises ; sinon, signale-le.
- Genre et accords : une chaîne composée avec une variable peut être fausse grammaticalement. Préfère une tournure neutre qui fonctionne quelle que soit la valeur.
- Cohérence stricte : un même élément porte le même nom partout. Suis les conventions de la plateforme (termes d'iOS, d'Android, de Windows en langue cible).
- Sans contexte, une chaîne courte est ambiguë (« Open » : verbe ou adjectif ?). Sers-toi de la clé, des chaînes voisines et des commentaires ; si le doute persiste, signale-le.

## 5. Données structurées (JSON, YAML, CSV, XML)

- Traduis les valeurs destinées à l'utilisateur, jamais les clés, les identifiants, les énumérations techniques ni les noms de champs.
- Le fichier rendu doit rester valide : mêmes clés, même ordre, même imbrication, échappements corrects (guillemets, antislash, entités).
- CSV : même nombre de colonnes et de lignes, même séparateur, guillemets autour des cellules qui contiennent le séparateur.
- Vérifie la validité en fin de travail si un outil est disponible (parseur JSON ou YAML).

## 6. Juridique et administratif

La précision prime sur le naturel. Une ambiguïté introduite peut avoir des conséquences.

- Utilise les termes consacrés du droit de la langue cible quand le concept existe à l'identique. Quand il n'existe pas (« trust », « common law », « société à responsabilité limitée »), garde le terme d'origine avec une traduction explicative entre parenthèses plutôt que de le remplacer par un faux équivalent.
- Ne fusionne pas et ne scinde pas les phrases si cela peut modifier la portée d'une clause. Garde la numérotation et les renvois.
- Traduis les termes définis de façon rigoureusement identique à chaque occurrence, majuscule comprise.
- Ne simplifie pas et n'interprète pas. Un passage obscur reste aussi obscur, et se signale.
- Précise une fois qu'une traduction certifiée peut être exigée pour un usage officiel.

## 7. Marketing et publicité

On traduit l'effet, pas la phrase : c'est de la transcréation.

- Demande-toi ce que le texte doit faire ressentir ou faire faire, puis écris en langue cible ce qui produit cet effet sur ce public.
- Adapte les références culturelles, l'humour et les exemples. Vérifie qu'un nom de produit ou un slogan n'a pas de connotation gênante en langue cible.
- Pour les accroches, propose deux ou trois variantes avec leur traduction littérale et ce que chacune privilégie.
- Respecte les contraintes de longueur (objet d'e-mail, bouton, annonce).
- Garde les mentions légales exactes : là, on revient à la fidélité stricte.

## 8. Sous-titres

- Garde les codes temporels et la numérotation intacts (SRT, VTT, ASS).
- Deux lignes au maximum par sous-titre, environ 42 caractères par ligne pour les alphabets latins. Condense si nécessaire : le spectateur doit avoir le temps de lire.
- Coupe les lignes aux frontières de sens, jamais entre un article et son nom.
- Langage oral naturel. Garde le registre de chaque locuteur.
- Ne déplace pas de contenu d'un sous-titre à l'autre, sauf si la syntaxe cible l'impose, et jamais au-delà du sous-titre voisin.

## 9. Académique et scientifique

- Suis la terminologie établie de la discipline en langue cible. En cas de doute sur un terme, garde l'original entre parenthèses à la première occurrence.
- Citations d'œuvres : utilise la traduction publiée si elle existe ; sinon traduis et indique « notre traduction ».
- Bibliographie : ne traduis pas les titres des références, sauf convention contraire de la revue ou demande.
- Garde les formules, symboles, unités et numéros de figures intacts. Traduis les légendes.
- Conserve la prudence de l'auteur : « suggère » ne devient pas « démontre », « peut » ne devient pas « est ».

## 10. Médical

- Dénominations communes internationales (DCI) pour les médicaments ; les noms de marque varient selon les pays, garde l'original en le signalant.
- Posologies, unités et valeurs : recopie avec la plus grande attention, sans conversion.
- Adapte le niveau de langue au lecteur : terminologie savante pour les professionnels, termes courants pour les patients.
- Signale une fois qu'une relecture par un professionnel est recommandée pour tout document destiné aux soins.

## 11. Correspondance

- Adapte les formules d'appel et de politesse aux usages de la langue cible plutôt que de les traduire mot à mot. Un « Best regards » ne se rend pas par la même formule dans un e-mail entre collègues et dans une lettre à une administration.
- Choisis le niveau de formalité d'après la relation entre les correspondants. S'il n'est pas clair, prends le plus formel des deux et signale-le.
- Garde la longueur et la franchise de l'original : ne rallonge pas un message direct par des précautions qui n'y étaient pas.

## 12. Presse et web

- Titres : suis les conventions de la langue cible (pas de majuscule à chaque mot en français, par exemple).
- Citations de personnes : traduis-les fidèlement, sans les embellir.
- Pour un contenu web, garde les liens, les ancres et les balises. Traduis les textes alternatifs des images et les métadonnées (titre, description) si elles sont fournies.
- Noms de fonctions et d'institutions : utilise l'appellation en usage dans la presse de la langue cible.
