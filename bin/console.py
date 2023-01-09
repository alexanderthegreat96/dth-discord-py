import click
from commands.generateCommand import generateCommand
from commands.generateCommand import appendCommandInConfig

print(r"""
     _ _   _               _ _                       _                      ____                      _      
  __| | |_| |__         __| (_)___  ___ ___  _ __ __| |      _ __  _   _   / ___|___  _ __  ___  ___ | | ___ 
 / _` | __| '_ \ _____ / _` | / __|/ __/ _ \| '__/ _` |_____| '_ \| | | | | |   / _ \| '_ \/ __|/ _ \| |/ _ \
| (_| | |_| | | |_____| (_| | \__ \ (_| (_) | | | (_| |_____| |_) | |_| | | |__| (_) | | | \__ \ (_) | |  __/
 \__,_|\__|_| |_|      \__,_|_|___/\___\___/|_|  \__,_|     | .__/ \__, |  \____\___/|_| |_|___/\___/|_|\___|
                                                            |_|    |___/""")

@click.group()
def commands():
    pass

@click.command()
@click.option('--name',default='my-command-name',help="Specify the command name")
@click.argument('command-name')
def generate(name,command_name):
    print('Generating command name: ' + command_name )
    print(generateCommand(command_name) + '\n')
    print(appendCommandInConfig(command_name))

commands.add_command(generate)


commands()