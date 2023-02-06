from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import discord
import time
import json
import os
from os import path
import importlib
import importlib.util
import sys
import types
from utils.user import user


class bot():
    def __init__(self, ):
        self.config = self.botConfig()
        self.bot = commands.Bot(command_prefix=self.config["bot-command-prefix"],
                                activity=discord.Activity(type=discord.ActivityType.listening,
                                                          name=self.config["bot-listens-to"],
                                                          description=self.config["bot-description"]),
                                intents=discord.Intents.all(), case_insensitive=True)
        self.commands = commands

    def botConfig(self):
        try:
            f = open('config/bot.json', 'r')
            try:
                data = json.load(f)
                return data['config']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def staffList(self):
        try:
            f = open('config/staff.json', 'r')
            try:
                data = json.load(f)
                return data['users']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def staffGroups(self):
        try:
            f = open('config/groups.json', 'r')
            try:
                data = json.load(f)
                return data['groups']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def str_to_class(self, field):
        try:
            identifier = getattr(sys.modules[field], field)
        except AttributeError:
            raise NameError("%s doesn't exist." % field)
        if isinstance(identifier, (types.ClassType, types.TypeType)):
            return identifier
        raise TypeError("%s is not a class." % field)

    def command_list(self):
        try:
            f = open('config/commands.json', 'r')
            try:
                data = json.load(f)
                return data['commands']
            except Exception as e:
                return False
        except Exception as e:
            return False

    def isArray(self, input):
        if (isinstance(input, list)):
            return True
        elif isinstance(input, dict):
            return True
        else:
            return False

    # imports given modules / python files allowing
    # dependency injection

    def path_import(self, absolute_path):
        spec = importlib.util.spec_from_file_location(absolute_path, absolute_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def checkIfItemIsNotEmpty(self, item):
        if (item is not None):
            return True
        elif (item != ''):
            return True
        else:
            return False

    def validateCommandInputs(self, inputs):

        if ('arguments' in inputs and len(inputs['arguments'])):
            for item in inputs['arguments']:
                self.validateCommandInputs(item)
        else:
            pass

    def generateArgumentAssociation(self, args, predefinedArguments={}, mainArg=''):
        associatedArguments = {}
        if (len(args) and len(predefinedArguments)):

            mergedArgs = []
            for item in predefinedArguments:
                mergedArgs.append(item)

                if ('required-arguments' in predefinedArguments[item] and predefinedArguments[item][
                    'required-arguments'] is not None):
                    for item in predefinedArguments[item]['required-arguments']:
                        mergedArgs.append(item)

            if (len(mergedArgs)):
                for item in mergedArgs:
                    if (item in args):
                        posIndex = args.index(item)
                        try:
                            associatedArguments[item] = args[posIndex + 1]
                        except Exception as e:
                            associatedArguments[item] = None

        else:
            if(args):
                associatedArguments = {mainArg: args[0]}
            else:
                associatedArguments = {mainArg: None}

        return associatedArguments


    def isBanned(self, ctx):
        userInfo = user(ctx)
        status = False

        if (path.exists('authorization/banned.py')):
            commandContents = self.path_import('authorization/banned.py')
            className = getattr(commandContents, 'banned')
            run = className(ctx, userInfo.getUserId)
            output = run.main()
            return output

    def authorize(self, ctx, groups=[]):
        if (groups):
            staffListGroups = self.staffGroups()
            userInfo = user(ctx)
            status = False
            for group in groups:
                if (group in staffListGroups):
                    if (path.exists('authorization/' + group + '.py')):
                        commandContents = self.path_import('authorization/' + group + '.py')
                        className = getattr(commandContents, group)
                        run = className(ctx, userInfo.getUserId())
                        output = run.main()
                        if(output == True):
                            return True

        else:
            status = True
        return status

    def checkUserInputs(self, inputArguments, arrayArguments={}, filledArguments={}, parentCommand='', subcommand='', ctx=None):

        status = True
        errors = []
        showRequiredArgumentsText = False
        showRequiredArgumentsSubcomandText = False
        if (filledArguments):
            if (len(arrayArguments)  and len(filledArguments)):
                if (any(item in arrayArguments for item in filledArguments)):
                    commandStatus = True
                    count1 = 0
                    for item in filledArguments:
                        count1 = count1 + 1
                        if (item in arrayArguments):
                            if ('hasValue' in arrayArguments[item] and arrayArguments[item]['hasValue']):
                                if (item in filledArguments):
                                    hasValue = arrayArguments[item]['hasValue']
                                    if (hasValue):
                                        if (filledArguments[item] is None):
                                            status = False
                                            commandStatus = False
                                            errors.append(
                                                str(count1) + '. Argument [' + item + '] MUST NOT be empty.')

                            if('authorization' in arrayArguments[item] and arrayArguments[item]['authorization'] is not None):
                                authorize = self.authorize(ctx,arrayArguments[item]['authorization'])
                                if(not authorize):
                                    commandStatus = False
                                    status = False
                                    errors.append(
                                        str(count1) + '. Argument [' + item + '] requires special privileges.')

                            if (commandStatus):
                                if ('required-arguments' in arrayArguments[item] and arrayArguments[item][
                                    'required-arguments'] is not None):
                                    count2 = 0
                                    for req in arrayArguments[item]['required-arguments']:
                                        count2 = count2 + 1
                                        if (req not in filledArguments):
                                            status = False
                                            showRequiredArgumentsSubcomandText = True
                                            errors.append(
                                                str(count2) + '. Required argument: [' + req + '] was not provided.')
                                        else:
                                            if (filledArguments[req] is None):
                                                status = False
                                                errors.append(
                                                    str(count2) + '. Required argument: [' + req + '] must not be empty!')
                else:
                    status = False
                    validArgs = ', '.join(arrayArguments.keys())
                    errors.append(
                        'You failed to provide required arguments. Valid arguments include: [' + validArgs + '].')

        else:
            if(arrayArguments is not None):

                count3 = 0


                for item in arrayArguments:
                    count3 = count3 + 1

                    if ('required' in arrayArguments[item] and arrayArguments[item]['required'] is not None):
                        required = arrayArguments[item]['required']
                        if (required):
                            status = False
                            showRequiredArgumentsText = True
                            errors.append(str(count3) + '. Required argument [' + item + '] not provided.')
                        else:

                            if('hasValue' in arrayArguments[item] and arrayArguments[item]['hasValue'] is not None):
                                hasValue = arrayArguments[item]['hasValue']
                                if (hasValue):
                                    status = False

                                    errors.append(str(count3) + '. Argument [' + item + '] must not be empty.')


        # else:
        #     status = False
        #     errors.append('No valid arguments were provided.')

        if (showRequiredArgumentsText):
            errors.insert(0, 'One of the following arguments need to be provided:\n')

        if (showRequiredArgumentsSubcomandText):
            errors.insert(0, 'The following arguments MUST BE provided:\n')

        if (status == False):
            errors.append('\nRefer to the command helper: [/' + parentCommand + ' ' + subcommand + ' help]')

        return {'status': status, 'errors': '\n'.join(errors)}

    def add_commands(self, commandName='dth'):
        @self.bot.before_invoke
        async def resetCooldown(ctx):
            # enable cooldown resets for staff members

            if (self.config['enable-reset-cooldowns']):
                staff = self.staffList()
                userInfo = user(ctx)
                if (str(userInfo.getUserId()) in staff['admin']):
                    return ctx.command.reset_cooldown(ctx)

                if (str(userInfo.getUserId()) in staff['moderator']):
                    return ctx.command.reset_cooldown(ctx)

                if (str(userInfo.getUserId()) in staff['root']):
                    return ctx.command.reset_cooldown(ctx)

        @self.bot.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandOnCooldown):
                seconds = error.retry_after
                await ctx.send('Your ability is on cooldown, retry in: <t:{}:R>'.format(int(time.time() + seconds)),
                               delete_after=seconds)

            # if isinstance(error, commands.CommandNotFound):  # or discord.ext.commands.errors.CommandNotFound as you wrote
            #     await ctx.send("```Unknown command. Run: [/dth help] for a full list of commands.```")
            # raise error

            # if isinstance(error, commands.MissingPermissions):
            #     await ctx.send("``` You do not have permissions to execute this command or this channel does not allow it. ```")
            #     raise error
            #
            # if isinstance(error, commands.CommandInvokeError):
            #     await ctx.send("``` Something went wrong. Most likely the channel does not allow embedding here. ```")
            #     raise error

            if (self.config['enable-global-errors']):
                raise error  # re-raise the error so all the errors will still show up in console

        # @

        command_list = self.command_list()
        counter = 1

        if (command_list):
            item = commandName
            thisCommand = item
            counter += 1
            if (path.exists('commands/' + item + '.py')):


                if ('arguments' in command_list[item] and command_list[item]['arguments'] is not None
                        and 'commands' not in command_list[item]):
                    arguments = command_list[item]['arguments']


                    @commands.cooldown(1, self.config['cooldown-duration'], commands.BucketType.user)
                    @self.bot.command(name=item, pass_context=True)
                    async def item(ctx, *args):
                        checkBan = self.isBanned(ctx)
                        if (checkBan):
                            await ctx.channel.send(
                                "```You have been banned from using any commands. If you think this is unfair, please contact the staff.```")
                        else:

                            if ('authorization' in command_list[thisCommand] and len(command_list[thisCommand]['authorization']) > 0):
                                authorization = command_list[thisCommand]['authorization']
                            else:
                                authorization = None

                            authorize = self.authorize(ctx, authorization)

                            authorize = True
                            authorization = []

                            if (authorize):

                                inputArguments = self.generateArgumentAssociation(args,command_list[thisCommand]['arguments'], commandName)
                                check = self.checkUserInputs(args, arguments, inputArguments, thisCommand)

                                if (check['status']):
                                    commandContents = self.path_import('commands/' + thisCommand + '.py')
                                    className = getattr(commandContents, thisCommand)
                                    run = className(self.bot, ctx, args, authorization, inputArguments)
                                    await run.main()
                                else:
                                    await ctx.channel.send("```" + check['errors'] + "```")

                            else:
                                if (authorization is not None):
                                    authorizedGroups = ','.join(authorization)
                                    await ctx.channel.send(
                                        '```You do not have permission to use this command. Only: [' + authorizedGroups + '] allowed.```')
                                else:
                                    await ctx.channel.send(
                                        '```You do not have permission to use this command.```')

                else:

                    @commands.cooldown(1, self.config['cooldown-duration'], commands.BucketType.user)
                    @self.bot.command(name=item, pass_context=True)
                    async def item(ctx, arg1=None, *args):
                        checkBan = self.isBanned(ctx)
                        if (checkBan):
                            await ctx.channel.send(
                                "```You have been banned from using any commands. If you think this is unfair, please contact the staff.```")
                        else:
                            if (arg1 is not None):
                                if (path.exists('commands/' + thisCommand + '/' + arg1 + '.py')):
                                    if ('commands' in command_list[thisCommand] and command_list[thisCommand][
                                        'commands'] is not None):
                                        subcommands = command_list[thisCommand]['commands']
                                        if (arg1 in subcommands):
                                            inputArguments = self.generateArgumentAssociation(args, subcommands[arg1][
                                                'arguments'], arg1)

                                            if ('authorization' in subcommands[arg1] and
                                                    subcommands[arg1]['authorization']):
                                                authorization = subcommands[arg1]['authorization']
                                            else:
                                                authorization = None

                                            authorize = self.authorize(ctx, authorization)
                                            if (authorize):
                                                if ('arguments' in subcommands[arg1] and subcommands[arg1][
                                                    'arguments'] is not None):
                                                    check = self.checkUserInputs(args, subcommands[arg1]['arguments'],
                                                                                 inputArguments, thisCommand, arg1,ctx)
                                                    if (check['status']):
                                                        commandContents = self.path_import(
                                                            'commands/' + thisCommand + '/' + arg1 + '.py')
                                                        className = getattr(commandContents, arg1)
                                                        run = className(self.bot, ctx, args, authorization,
                                                                        inputArguments)
                                                        await run.main()
                                                    else:
                                                        await ctx.channel.send("```" + check['errors'] + "```")
                                                else:
                                                    commandContents = self.path_import(
                                                        'commands/' + thisCommand + '/' + arg1 + '.py')
                                                    className = getattr(commandContents, arg1)

                                                    if (args):
                                                        sendInput = {arg1: args[0]}
                                                    else:
                                                        sendInput = {arg1: None}

                                                    run = className(self.bot, ctx, args, authorization, sendInput)
                                                    await run.main()
                                            else:
                                                if (authorization is not None):
                                                    authorizedGroups = ','.join(authorization)
                                                    await ctx.channel.send(
                                                        '```You do not have permission to use this command. Only: [' + authorizedGroups + '] allowed.```')
                                                else:
                                                    await ctx.channel.send(
                                                        '```You do not have permission to use this command.```')
                                        else:
                                            await ctx.channel.send(
                                                "```The provided argument was not implemented. Refer to [" + thisCommand + " help] for more information.```")
                                    else:
                                        # no subcomands available
                                        # return error
                                        await ctx.channel.send(
                                            "```The provided command has an empty array of sub items. Either fill them or remove the key entirely. Refer to [" + thisCommand + " help] for more information.```")
                                else:
                                    await ctx.channel.send("```[" + arg1 + "] is not a valid command endpoint.```")
                            else:

                                subcommands = ', '.join(command_list[thisCommand]['commands'])
                                await ctx.channel.send("```No command line arguments specified.\n"
                                                       "This command contains a number of sub commands and at least one needs to be specified.\n"
                                                       "Use: [" + self.config[
                                                           'bot-command-prefix'] + "" + thisCommand + " help]```")

    def boot(self):
        print(self.config['bot-name'] + ' started running\nawaiting user input...')
        self.bot.run(self.config['bot-token'])
