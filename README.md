# Ma configuration Claude Code

Mes règles de travail, mes réglages et mes skills pour [Claude Code](https://claude.com/claude-code). Je travaille sur plusieurs ordinateurs ; ce dépôt leur sert de référence commune.

| Fichier | Ce que c'est |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Mes règles de travail. Lu au démarrage de chaque session, dans tous les projets ; ses consignes priment sur le comportement par défaut. Il décrit **comment je veux qu'on travaille** — pas ce que mes projets contiennent. |
| [`settings.json`](settings.json) | Mes réglages : modèle, plugins activés, thème, marketplaces, et les hooks qui tournent à chaque session. Le bloc `autoMode.environment` est retiré de la version publiée : il décrit la machine et un dépôt privé, et il se régénère localement. |
| [`skills/`](skills) | Les quatre skills que j'ai écrits. Les skills tiers et ceux synchronisés depuis claude.ai ne sont pas ici : ils ne sont pas de moi. |
| [`claude-md-controle.sh`](claude-md-controle.sh) | Le contrôle de démarrage décrit plus bas. |

## Les skills

- **`chef`** — le rôle de maître d'œuvre : un agent par lot, un relecteur après chacun, un registre.
- **`chef-conseil`** — l'escalade de réflexion quand un arbitrage dépasse l'orchestrateur : argent, sécurité, concurrence, migration de données.
- **`traduction-universelle`** — traduction de haute qualité, tous contenus et toutes langues.
- **`turning-mistakes-into-checks`** — transformer une faute qu'on vient de me signaler en garde-fou durable.

Les hooks déclarés dans `settings.json` appellent `~/.claude/chef-hooks.sh`, qui n'est pas publié ici.

## Les règles du CLAUDE.md

| Règle | En une phrase |
|---|---|
| **Ajout de skills depuis un lien** | Lire le skill en entier, le comparer à l'existant, et savoir me dire non avant d'installer. |
| **Je suis maître d'ouvrage** | Je décide et je valide ; Claude dirige des agents spécialisés et n'implémente pas lui-même. Un lot d'une seule touche se fait directement, sans cérémonie. |
| **Le plus petit changement complet** | La plus petite solution qui règle *tout* le problème, rien que je n'aie demandé. Imposé par le plugin [ponytail](https://github.com/DietrichGebert/ponytail). |
| **Vérifier avant d'affirmer** | Ne rien déclarer qui marche sans avoir lancé la commande et lu la sortie. Un rapport d'agent est une affirmation, pas une preuve. |

Une consigne traverse les quatre : **les règles descendent jusqu'aux agents**. Un agent dispatché n'hérite ni de ce fichier ni des hooks de la session, donc chaque brief doit les rappeler explicitement.

## Pourquoi c'est public

Parce que ces règles et ces skills peuvent servir à d'autres, et qu'aucun secret, mot de passe ni clé ne figure dans ces fichiers.

## Synchronisation entre machines

La source de vérité reste `~/.claude/` sur chaque machine ; ce dépôt n'est pas cloné en local, pour éviter deux copies qui divergent.

Un contrôle au démarrage de session compare la config locale à celle du dépôt et **signale** une différence. Il n'écrase jamais rien : avec plusieurs PC, l'une ou l'autre version peut être la plus récente, et c'est à moi de trancher.

Il surveille `CLAUDE.md`, `settings.json`, les skills et le script lui-même, et distingue trois cas : contenu différent, publié mais absent de la machine, présent sur la machine mais pas publié. Pour `settings.json` il ignore le bloc `autoMode.environment`, propre à chaque poste. Une seule requête à l'API GitHub, comparaison par empreinte ; muet quand tout concorde, muet hors ligne.

Publier la version de cette machine :

```sh
gh api --method PUT /repos/CedricHenault/claude-md/contents/CLAUDE.md \
  -f message="mise à jour" \
  -f content="$(base64 -i ~/.claude/CLAUDE.md | tr -d '\n')" \
  -f sha="$(gh api /repos/CedricHenault/claude-md/contents/CLAUDE.md -q .sha)"
```

Le `sha` est obligatoire pour une mise à jour : il empêche d'écraser une modification faite entre-temps depuis une autre machine.

### Installer le contrôle sur une nouvelle machine

Le contrôle est le script [`claude-md-controle.sh`](claude-md-controle.sh) de ce dépôt. Sur un PC neuf :

```sh
curl -fsSL https://raw.githubusercontent.com/CedricHenault/claude-md/main/claude-md-controle.sh \
  -o ~/.claude/claude-md-controle.sh && chmod +x ~/.claude/claude-md-controle.sh
```

Puis le déclarer dans `~/.claude/settings.json`, dans `hooks.SessionStart` :

```json
{ "type": "command", "command": "$HOME/.claude/claude-md-controle.sh", "timeout": 10,
  "statusMessage": "Contrôle du CLAUDE.md partagé" }
```

Le script se tait quand les deux versions sont identiques, quand il n'y a pas de réseau et quand il n'y a pas de `CLAUDE.md` local. Il ne parle que s'il y a une vraie différence.
