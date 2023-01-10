__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "stable"
__name__ = "dth-labs-discord"

from core.bot import bot

system = bot()
commands = system.command_list()

if(commands):
    for command in commands:
        system.add_commands(command)
system.boot()

