class track:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments

    async def main(self):
        print(self.inputArguments)
        await self.ctx.channel.send("```This is the track.py command output within commands/dth folder.```")