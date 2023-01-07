class comment:
    def __init__(self,ctx,args,authorization,inputArguments):
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments

    async def main(self):
        await self.ctx.channel.send("```This is the comment.py command output within commands/dth folder.```")