class track:
    def __init__(self,ctx,args):
        self.ctx = ctx
        self.args = args

    def main(self):
        await self.ctx.channel.send("```This is the track.py command output within commands/dth folder.")