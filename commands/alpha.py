class alpha:
    def __init__(self,ctx,args,authorization=None, arguments=None):
        self.ctx = ctx
        self.args = args
        self.authorization = authorization
        self.arguments = arguments


    def main(self):
        return 'Hello,this is the alpha command'

