class dth:
    def __init__(self,ctx,args,authorization=None, arguments=None):
        self.ctx = ctx
        self.args = args
        self.authorization = authorization
        self.arguments = arguments


    async def main(self):
        await self.ctx.channel.send("```This is the dth.py command output within commands folder.```")

