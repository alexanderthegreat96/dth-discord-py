import discord
from typing import Dict
from utils.utils import utils

class embed:
    def __init__(self, title="My Embed", description="", data=[], color="blue"):
        self.data = data
        self.color = color
        self.title = title
        self.description = description


    def colorInstances(self):
        match self.color:
            case 'blue':
                return discord.Color.blue()
            case 'green':
                return discord.Color.green()
            case 'yellow':
                return discord.Color.yellow()
            case 'black':
                return discord.Color.dark_gray()
            case 'dark_red':
                return discord.Color.dark_red()
            case 'dark_green':
                return discord.Color.dark_green()
            case 'dark_blue':
                return discord.Color.dark_blue()
            case _:
                return  discord.Color.dark_gray

    def make(self):
        if (self.data):
            general = discord.Embed(title=self.title,
                                    description=self.description,
                                    color=self.colorInstances())
            if (isinstance(self.data, Dict)):

                split = utils.splitArray(self.data,5)

                for item in self.data:
                    general.add_field(name=item, value = self.data[item], inline=False)
            else:
                for item in self.data:
                    general.add_field(name=item, value=item, inline=False)
        else:
            return None