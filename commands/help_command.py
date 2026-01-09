from commands.command import Command

help_message = (
    "Unknown command. Usage:\n"
    "!group        - Show current league tables\n"
    "!fixtures     - Show next week's fixtures\n"
    "!results      - Show latest round and all previous results\n"
    "!all-fixtures - Show complete fixture list\n"
    "!help         - Show this help message"
)

class HelpCommand(Command):
    def run(self):
        return help_message