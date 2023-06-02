import discord
from discord import app_commands
from discord.ext import commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(description='Creates a ticket to communicate with the moderators')
    async def ticket(self, interaction:discord.Interaction):
        pass