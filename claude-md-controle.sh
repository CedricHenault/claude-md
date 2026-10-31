#!/bin/sh
# Compare la config locale (~/.claude) au dépôt public CedricHenault/claude-md.
# Ne réécrit JAMAIS : avec plusieurs PC, l'une ou l'autre version peut être la plus récente.
exec python3 -I - <<'PY'
import hashlib, json, os, sys, urllib.request

BASE = os.path.expanduser("~/.claude")
TREE = "https://api.github.com/repos/CedricHenault/claude-md/git/trees/main?recursive=1"
# Publié mais sans équivalent local à surveiller.
IGNORE = {"README.md"}

def blob_sha(data):
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()

def canon_settings(data):
    # Le dépôt porte volontairement un autoMode.environment expurgé : il décrit la machine.
    try:
        d = json.loads(data)
        d.get("autoMode", {}).pop("environment", None)
        return json.dumps(d, sort_keys=True).encode()
    except Exception:
        return data

try:
    req = urllib.request.Request(TREE, headers={"Accept": "application/vnd.github+json",
                                                "User-Agent": "claude-md-controle"})
    tree = json.load(urllib.request.urlopen(req, timeout=6))["tree"]
except Exception:
    sys.exit(0)

distants = {e["path"]: e["sha"] for e in tree
            if e["type"] == "blob" and e["path"] not in IGNORE}
if not distants:
    sys.exit(0)

differe, manquant = [], []
for path, sha in sorted(distants.items()):
    local = os.path.join(BASE, path)
    if not os.path.isfile(local):
        manquant.append(path)
        continue
    with open(local, "rb") as f:
        data = f.read()
    if path == "settings.json":
        with urllib.request.urlopen(
            "https://api.github.com/repos/CedricHenault/claude-md/contents/settings.json",
            timeout=6) as r:
            import base64
            dist = base64.b64decode(json.load(r)["content"])
        if canon_settings(data) != canon_settings(dist):
            differe.append(path + " (hors bloc environment, propre à la machine)")
        continue
    if blob_sha(data) != sha:
        differe.append(path)

# Fichier présent ici mais pas publié, dans un dossier de skill que le dépôt connaît déjà.
publies = {os.path.dirname(p) for p in distants if p.startswith("skills/")}
dossiers = {"/".join(p.split("/")[:2]) for p in distants if p.startswith("skills/")}
en_trop = []
for d in sorted(dossiers):
    racine = os.path.join(BASE, d)
    for dirpath, _, noms in os.walk(racine):
        for n in noms:
            if n.startswith("."):
                continue
            rel = os.path.relpath(os.path.join(dirpath, n), BASE)
            if rel not in distants:
                en_trop.append(rel)

if not (differe or manquant or en_trop):
    sys.exit(0)

print("Configuration Claude Code : cette machine et le dépôt CedricHenault/claude-md DIVERGENT.")
if differe:
    print("  Contenu différent : " + ", ".join(differe))
if manquant:
    print("  Publié mais absent ici : " + ", ".join(manquant))
if en_trop:
    print("  Présent ici mais pas publié : " + ", ".join(sorted(en_trop)))
print("À FAIRE : signale-le dès ta première réponse, montre le diff du ou des fichiers concernés,")
print("et demande quelle version garder. N'écrase rien sans accord — un autre PC peut être en avance.")
PY
