# Starship for prompt
eval "$(starship init bash)"

# Affirmation for the day
# Although this happens on each hour, it's a nice reminder
source ~/.config/bash/affirmation.sh

# Personal project assitant to manage some tasks like:
# - Start a project
# - Run tests
alias a="py ~/cli/assistant/app.py"
alias assistant="py ~/cli/assistant/app.py"