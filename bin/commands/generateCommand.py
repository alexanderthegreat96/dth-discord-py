from os import path
import os
import json
from from_root import from_root

def appendCommandInConfig(command='command'):
    if(not path.exists(from_root('config/commands.json'))):
        with open(from_root('config/commands.json'), 'w') as f:
            json.dump({'commands' : {}}, f, indent=2)
    try:
        f = open(from_root('config/commands.json'), 'r')
        try:
            data = json.load(f)

            if ('/' in command):
                filePath = os.path.basename(command)
                dirPath = os.path.dirname(command)

                if(dirPath not in data['commands']):
                    data["commands"].update({dirPath: {"authorization": [], "arguments": {}}})

                    with open(from_root('config/commands.json'), 'w') as f:
                        json.dump(data, f, indent=2)

                if('commands' not in data['commands'][dirPath]):
                    data['commands'][dirPath]['commands'] = {}

                if(filePath not in data['commands'][dirPath]['commands']):

                    data['commands'][dirPath]['commands'][filePath] = {}
                    data['commands'][dirPath]['commands'][filePath] = {"authorization":[], "arguments":{}}


                    if ('arguments' in data['commands'][dirPath]):
                        del data['commands'][dirPath]['arguments']
                    # data['commands'][dirPath]['commands'][filePath].append({"authorization":[], "arguments":[]})
                    #
                    with open(from_root('config/commands.json'), 'w') as f:
                        json.dump(data, f, indent=2)
                return 'Command configuration dumped.'

            else:
                if (command not in data['commands']):
                    append = {
                        command: {
                            "authorization": [],
                            "arguments": {},
                        }
                    }
                    data["commands"].update(append)

                    with open(from_root('config/commands.json'), 'w') as f:
                        json.dump(data,f,indent=2)

                return 'Command configuration dumped.'

        except Exception as e:
            print(str(e))
    except Exception as e:
        print(str(e))


def generateCommand(command='my-command'):
    if ('/' in command):
        filePath = os.path.basename(command)
        dirPath = os.path.dirname(command)
        if(not path.exists('commands/' + dirPath + '/' + filePath + '.py')):

            if not os.path.exists('commands/'+ dirPath):
                os.makedirs('commands/' + dirPath)
            else:
                pass


            content = r"""import discord
import asyncio

class """+filePath+""":
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the """+filePath+""" command output within commands folder.```")
    """

            openFile = open('commands/' + dirPath + '/' + filePath + '.py', "w")
            openFile.write(content)
            openFile.close()

        if(not path.exists('commands/' + dirPath + '.py')):

            fileContents = r"""import discord
import asyncio

class """ + dirPath + """:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the """ + dirPath + """ command output within commands folder.```")
    """


            f = open('commands/' + dirPath + '.py', "w")
            f.write(fileContents)
            f.close()

        return "Command file " + filePath + ".py created in commands/" + dirPath
    else:
        if (path.exists('commands/' + command + '.py')):
            return 'Could not generate command file. The file [commands/'+command+'.py] already exists. Remove it and try again.'
        fileContents = r"""import discord
import asyncio

class """ + command.replace('-','') + """:
    def __init__(self, bot, ctx, args, authorization, inputArguments):
        self.bot = bot
        self.ctx = ctx
        self.authorization = authorization
        self.args = args
        self.inputArguments = inputArguments


    async def main(self):
        await self.ctx.channel.send("```This is the """ + command + """ command output within commands folder.```")
    """

        f = open('commands/' +command+ '.py', "w")
        f.write(fileContents)
        f.close()

        return "Command file " + command + ".py created in commands/"