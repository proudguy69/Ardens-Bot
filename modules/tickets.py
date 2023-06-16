import discord
from discord import app_commands
from discord.ext import commands
from discord import ui
from discord.interactions import Interaction

# ticket view
class ticketSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Report User", description="Select this if you want to report a user"),
            discord.SelectOption(label="General Question", description="Select this if you have a general question"),
            discord.SelectOption(label="Other", description="Select this if the above options don't fit")
        ]
        
        super().__init__(custom_id="ticketSelectPrompt", min_values=1, max_values=1, options=options)
    
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f'You selected {self.values[0]}!', ephemeral=True)


class ticketSelView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ticketSelect())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='prompt')
    async def prompt(self, ctx:commands.Context):
        if ctx.author.id != 729873770990534766: return
        await ctx.send('test!', view=ticketSelView())