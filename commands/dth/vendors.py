class vendors:
    def __init__(self,ctx,args,authorization,inputArguments):
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments

    def main(self):
        print('hello')
        return "this is the vendors file. you are searching for : "