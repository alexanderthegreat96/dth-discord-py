__author__ = "alexanderdth"

__license__ = "MIT"
__maintainer__ = "alexanderdth"
__status__ = "stable"
__name__ = "dth-labs-discord"

from core.bot import bot

system = bot()
system.add_commands('dth')
system.add_commands('alpha')
system.boot()

