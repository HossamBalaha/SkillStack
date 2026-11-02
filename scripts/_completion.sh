# SkillStack shell completion for Skill.py.
#
# Source this file from your shell rc to enable tab-completion for the
# SkillStack CLI:
#
#   bash:  source scripts/_completion.sh    (in ~/.bashrc)
#   zsh:   source scripts/_completion.sh    (in ~/.zshrc, after `autoload -U +X bashcompinit && bashcompinit`)
#
# The completion offers the seven SkillStack subcommands and the names of
# skills where appropriate:
#
#   Skill.py list             — no arguments
#   Skill.py search <query>   — free text
#   Skill.py show <skill>      — skill name
#   Skill.py validate <skill>  — skill name
#   Skill.py graph             — no arguments
#   Skill.py tags              — no arguments
#   Skill.py health            — no arguments
#
# The skill-name completion uses `python scripts/Skill.py list` once and
# caches the result in the _SKILLSTACK_SKILLS environment variable so the
# completion stays fast on repeated invocations.

# Resolve the directory of this file relative to the sourcing shell so the
# completion works no matter what the current working directory is.
_SkillStackScriptDir="$(cd "$(dirname "${BASH_SOURCE[0]:-${(%):-%x}}")" 2>/dev/null && pwd)"

# Cached list of every skill name (filled lazily on first completion).
_SkillStackSkillList=""

# Refresh the cached skill list by invoking the Skill.py CLI once.
_SkillStackRefreshSkills() {
  # Bail out silently when the CLI script is missing.
  if [ ! -f "$_SkillStackScriptDir/Skill.py" ]; then
    return 0
  fi
  # Run the list subcommand and extract skill names from the rich output.
  # The CLI prints "  <skill-name>" lines under each theme panel; we keep
  # only the leading-word of every indented line.
  _SkillStackSkillList="$(python "$_SkillStackScriptDir/Skill.py" list 2>/dev/null \
    | sed -n 's/^  \([a-z0-9-]*\).*/\1/p' \
    | sort -u)"
}

# Main completion function bound to the `Skill.py` command name.
_SkillStackComplete() {
  # Words being typed on the current command line.
  local cur prev words cword
  # Initialize the word-splitting variables for both bash and zsh.
  if [ -n "$ZSH_VERSION" ]; then
    # zsh's bashcompinit exposes COMP_WORDS / COMP_CWORD.
    cur="${words[$((cword + 1))]}"
    prev="${words[$((cword))]}"
  else
    _init_completion 2>/dev/null || {
      # Fallback for bash without bash-completion installed.
      cur="${COMP_WORDS[COMP_CWORD]}"
      prev="${COMP_WORDS[COMP_CWORD - 1]}"
      words=("${COMP_WORDS[@]}")
      cword="$COMP_CWORD"
    }
  fi

  # The seven subcommands the Skill.py CLI exposes.
  local subcommands="list search show validate graph tags health"

  # First argument: complete from the subcommand list.
  if [ "$cword" -eq 1 ]; then
    # Filter the subcommand list by the current word being typed.
    local matches
    matches="$(echo "$subcommands" | tr ' ' '\n' | grep -E "^${cur}" | sort -u)"
    # Hand the matches back to the shell as completions.
    COMPREPLY=($(compgen -W "$matches" -- "$cur"))
    return 0
  fi

  # Resolve the active subcommand (the second word on the command line).
  local subcommand="${words[1]}"

  # Per-subcommand completion for arguments.
  case "$subcommand" in
    list | graph | tags | health)
      # These subcommands take no arguments; offer nothing.
      COMPREPLY=()
      ;;
    search)
      # Free-text query; offer nothing so the user types the query.
      COMPREPLY=()
      ;;
    show | validate)
      # These subcommands take a skill name; offer the cached skill list.
      # Lazily refresh the cache when empty.
      if [ -z "$_SkillStackSkillList" ]; then
        _SkillStackRefreshSkills
      fi
      # Filter the skill list by the current word being typed.
      COMPREPLY=($(compgen -W "$_SkillStackSkillList" -- "$cur"))
      ;;
    *)
      # Unknown subcommand; fall back to the subcommand list.
      COMPREPLY=($(compgen -W "$subcommands" -- "$cur"))
      ;;
  esac

  return 0
}

# Bind the completion function to the Skill.py invocation patterns the
# user is likely to type: `Skill.py`, `python scripts/Skill.py`,
# `python3 scripts/Skill.py`, and `./scripts/Skill.py`.
complete -F _SkillStackComplete Skill.py 2>/dev/null
complete -F _SkillStackComplete -o default python 2>/dev/null
complete -F _SkillStackComplete -o default python3 2>/dev/null

# When sourced under zsh, expose bashcompinit if the user has not yet
# loaded it so the `complete` builtin above works.
if [ -n "$ZSH_VERSION" ]; then
  # The `complete` calls above are no-ops in zsh without bashcompinit.
  autoload -U +X bashcompinit 2>/dev/null && bashcompinit 2>/dev/null
  # Re-bind now that bashcompinit is available.
  complete -F _SkillStackComplete Skill.py 2>/dev/null
  complete -F _SkillStackComplete -o default python 2>/dev/null
  complete -F _SkillStackComplete -o default python3 2>/dev/null
fi

# Hint to the user that completion is loaded.
echo "SkillStack completion loaded for: list search show validate graph tags health" >&2
