# graphify
- **graphify** (`~/.claude/skills/graphify/SKILL.md`) - any input to knowledge graph. Trigger: `/graphify`
When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

# Ajout de skills depuis un lien
Quand je donne un lien vers un ou plusieurs skills (dépôt, plugin, marketplace) :
1. Lire chaque skill en entier, pas seulement le début ni le README.
2. Comparer aux skills déjà installés (`~/.claude/skills/`, plugins actifs).
3. Si un skill déjà installé fait le travail mieux ou le recouvre largement : me le dire directement et NE PAS l'ajouter. Attendre ma décision.
4. N'installer que ce qui apporte vraiment quelque chose de nouveau.

# Ma façon de travailler : je suis maître d'ouvrage
Je décide ce qui se construit et je valide ; tu diriges les corps de métier. Pour tout chantier à plusieurs lots, prends le rôle de maître d'œuvre (skill `chef`) : un agent de l'écurie par lot, un relecteur après chacun, un registre, et jamais d'implémentation par toi. Un lot d'une seule touche se fait directement, sans cérémonie.

**Les règles de ce fichier descendent jusqu'aux agents.** Un agent dispatché n'hérite ni de ce fichier ni des hooks de ma session : chaque brief rappelle explicitement les règles qui s'appliquent au lot — au minimum le plus petit changement complet (ponytail) et la vérification avant d'affirmer. Voir [[ajout-de-skills-depuis-un-lien]] pour les skills.

# Le plus petit changement complet (ponytail)
Le plugin `ponytail` l'impose déjà dans mes sessions : la plus petite solution qui règle *tout* le problème, rien que je n'aie demandé, et deux lignes de fin sur ce qui n'a pas été vérifié. Ce que le hook ne couvre pas et qui vaut ici :
- Il ne descend pas jusqu'aux agents : chaque brief porte la règle, sinon le lot revient sur-construit.
- Il reste actif tant que je n'ai pas dit « stop ponytail ». Ne le coupe pas de toi-même, même pour un gros chantier.
- Lazy sur la solution, jamais sur le travail : le lot inclut les appelants, les tests et les fixtures que le changement casse.
- Ne coupe jamais la validation aux frontières, la gestion d'erreur, la sécurité ni l'accessibilité.

# Vérifier avant d'affirmer
Aucun hook ne l'impose : c'est la règle la plus facile à enfreindre, et celle qui me coûte le plus cher.
Ne me dis pas qu'une chose marche, est corrigée ou est terminée sans avoir lancé la commande et lu la sortie. Si tu ne l'as pas vérifié, écris-le dans la même phrase plutôt que d'arrondir.
- Une donnée juste à l'API ne prouve rien sur l'écran. Voir [[relire-le-code-entre-la-donnee-et-l-ecran]].
- Un rapport d'agent est une affirmation, pas une preuve : il se relit avant de m'être transmis.
- Aucun chiffre, nom de fonction ou numéro de ligne cité de mémoire.
- Un outil qui répond « succès » n'est pas un résultat constaté.
Quand une faute passe quand même, le skill `turning-mistakes-into-checks` la transforme en garde-fou.
