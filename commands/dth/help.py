class help:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments

    async def main(self):
        await self.ctx.channel.send("```This is the help.py command output within commands/dth folder.```")