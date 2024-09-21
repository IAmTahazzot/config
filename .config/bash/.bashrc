# ---------------------------------------------------------------------
# Alias 1.0.0
# Date: Sep 21,2024:11:05PM
# ---------------------------------------------------------------------
#
# Useful alias to make some exasperating task simpler
#

# GitBash
alias .="vim ~/.bashrc"
alias load="source ~/.bashrc"

# Miscellaneous
alias c="clear"
alias h="history"
alias path='echo -e ${PATH//:/\\n}'


# Navigation
alias home="cd ~"
alias desktop="cd ~/Desktop"
alias back="cd -"
alias ~="cd ~"
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."


# Git
alias gfuck="git reset --hard HEAD"
alias glog="git log --oneline --graph --all --decorate"
alias gb="git branch -vv"
alias gs="git status"
alias gc="git commit"


# ---------------------------------------------------------------------
# Language and framework specific
# 
# - C++
# - Python
# - TypeScript
# - Node
# ---------------------------------------------------------------------
#
# Just to make the workload a bit easier mentally

# python
alias py='python3'

# Node
alias npm='npm --no-progress'
alias dev='npm run dev'

# Starship initiator
eval "$(starship init bash)"
