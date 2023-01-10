class server:
    def __init__(self,ctx,discord):
        if ctx.channel.type == discord.ChannelType.private:
            self.discord_name = 'direct_message'
            self.serverid = 0
            self.servername = "direct_message"
        else:
            self.servername = ctx.message.guild.name
            self.serverid = ctx.message.guild.id
            self.discord_name = ctx.message.guild.name

    def getServerName(self):
        return self.servername

    def getServerId(self):
        return self.serverid