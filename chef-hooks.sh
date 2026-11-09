#!/usr/bin/env bash
# Garde-fous mecaniques du skill chef (~/.claude/skills/chef/SKILL.md).
# Les branches ecriture / dispatch / rondes ne s'activent que si
# ~/.claude/chef-actif contient l'id de la session en cours : un drapeau laisse
# par une session morte ne matche plus jamais, donc il expire tout seul.
#
# ET SEULEMENT SUR LE FIL PRINCIPAL. Un sous-agent herite du session_id de la
# session qui l'a dispatche — c'est documente : « When a subagent calls a tool,
# tool events such as PreToolUse and PostToolUse fire the same configured hooks
# as in the main conversation ». Le drapeau seul bloquait donc l'agent exactement
# comme le maitre d'oeuvre, et aucun lot ne pouvait etre ecrit par personne.
# `agent_id` est le discriminant documente : « Unique identifier for the subagent
# or in-process teammate the hook fires in » — vide sur le fil principal, rempli
# dans un sous-agent ou un coequipier en processus.
# Ne pas tester `agent_type` a sa place : il est aussi rempli sur le fil
# principal quand la session est lancee avec --agent.
# Origine : incident reel du 2026-11-08, chantier « films sur les pieces ».
set -uo pipefail
payload=$(cat)
sid=$(printf '%s' "$payload" | jq -r '.session_id // empty')
agent=$(printf '%s' "$payload" | jq -r '.agent_id // empty')
actif=0
[ -z "$agent" ] && [ -n "$sid" ] && [ -f "$HOME/.claude/chef-actif" ] \
  && grep -qxF "$sid" "$HOME/.claude/chef-actif" && actif=1

deny() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",
    permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

case "${1:-}" in
  ecriture)
    [ "$actif" = 1 ] || exit 0
    f=$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty')
    [ -n "$f" ] || exit 0
    case "$f" in
      *.superpowers/sdd/*|"$HOME"/.claude/*|/tmp/*|/private/tmp/*) exit 0 ;;
    esac
    deny "Maitre d'oeuvre : tu n'ecris pas le code. Ce fichier appartient a un lot — redige un brief et dispatche un agent de l'ecurie. Tes seules zones d'ecriture : .superpowers/sdd/, ~/.claude/, le scratchpad."
    ;;

  dispatch)
    [ "$actif" = 1 ] || exit 0
    m=$(printf '%s' "$payload" | jq -r '.tool_input.model // empty')
    [ -n "$m" ] && exit 0
    deny "Dispatch sans modele : sans 'model' explicite tu herites du defaut de la definition, qui n'a pas ete ecrit pour ce lot. Ajoute model — haiku (commit, renommage), sonnet (code mecanique), opus (argent, securite, concurrence, migration, architecture). Seuls ces alias sont acceptes, jamais un identifiant complet."
    ;;

  rondes)
    # chef : « Trois allers-retours avec le meme agent, au maximum. »
    [ "$actif" = 1 ] || exit 0
    to=$(printf '%s' "$payload" | jq -r '.tool_input.to // empty')
    [ -n "$to" ] || exit 0
    c="$HOME/.claude/chef-compteur-$sid.txt"
    n=$(grep -cxF "$to" "$c" 2>/dev/null) || n=0
    if [ "$n" -ge 3 ]; then
      deny "Quatrieme aller-retour avec $to : la regle est trois. Le defaut n'est plus dans son travail — c'est le brief, le modele ou le decoupage. Monte d'un cran et dis au nouvel agent que le lot a deja ete tente."
    fi
    echo "$to" >> "$c"
    exit 0
    ;;

  ecurie)
    f=$(printf '%s' "$payload" | jq -r '.tool_response.filePath // .tool_input.file_path // empty')
    case "$f" in "$HOME"/.claude/agents/*) ;; *) exit 0 ;; esac
    out=$("$HOME/.claude/agents/verifier-ecurie.sh" 2>&1) || true
    [ -n "$out" ] || out="inventaire indisponible"
    jq -n --arg o "$out" '{hookSpecificOutput:{hookEventName:"PostToolUse",
      additionalContext:("verifier-ecurie.sh apres modification de l ecurie :\n"+$o)}}'
    ;;
esac
