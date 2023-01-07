class user:
    def __init__(self, ctx):
        self.user_id = ctx.message.author.id
        self.discriminator = ctx.author.discriminator
        self.username = ctx.message.author.name
        self.full_username = self.username + "#" + self.discriminator

    def getUserId(self):
        return self.user_id

    def getDiscriminator(self):
        return self.discriminator

    def getUsername(self):
        return self.username

    def getFullUsername(self):
        return self.full_username

