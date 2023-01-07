class comment:
    def __init__(self,ctx,args,authorization,inputArguments):
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments

    def main(self):
        return ("This is the username: ")