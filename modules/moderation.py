import discord
from discord import app_commands
from discord.ext import commands
from .database import ModerationDatabase as mdb
import time
import math

class Moderation(commands.Cog):
    def __init__(self):
        super().__init__()
    
    @app_commands.command()
    async def createmodtables(self, interaction:discord.Interaction):
        if interaction.user.id != 729873770990534766: return  await interaction.response.send_message('You cant edit the database')
        mdb.createModerationTables()
        await interaction.response.send_message('Tables have been created!')
        
    @app_commands.command()
    async def deletemodtables(self, interaction:discord.Interaction):
        if interaction.user.id != 729873770990534766: return  await interaction.response.send_message('You cant edit the database')
        mdb.DeleteModerationTables()
        await interaction.response.send_message('Tables have been Deleted!')
    
    
    
    #actual moderation commands commands
    @app_commands.command(description='Warns a user for given reason.')
    @app_commands.describe(user='The user you want to warn')
    async def warn(self, interaction:discord.Interaction, user:discord.Member, reason:str, hidden:bool=True):
        if interaction.user.guild_permissions.manage_messages == False: await interaction.response.send_message('Cant warn users'); return
        date = math.floor(time.time())
        mdb.CreateWarnRecord(user.id, date, reason, interaction.user.id)
        embed = discord.Embed(title=f"Warned {user.name}", description=f"✅ I have Succesfully warned {user.mention} for: `{reason}`", color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=hidden)
        # ========== LOG HERE ==========
        embed = discord.Embed(title='New Infraction', description=f'Type: Warn\nUser: {user.mention}\nModerator: {interaction.user.mention}')
        
    @app_commands.command(description="View the warns of another user")
    @app_commands.describe(user='The user you want to view the warns of')
    async def warns(self, interaction:discord.Interaction, user:discord.Member, hidden:bool=True):
        records = mdb.GetWarnRecords('*', user.id)
        if len(records) == 0: await interaction.response.send_message('This user has no warns!'); return
        
        embed = discord.Embed(title=f"Warns for {user.name}", color=0xff0000)
        for count, value in enumerate(records):
            if count <= 4:
                embed.add_field(name=f'Record {count+1}', value=f"Infraction ID: `{value[0]}`\nReason:`{value[3]}`\nWarned by: <@{value[4]}>\nWarned @ <t:{value[2]}>", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=hidden)
    
    
    
    
    
    #flag commands
    @app_commands.command(description='flags a user')
    @app_commands.describe(
        user = 'The user you want to flag, if any'
    )
    async def flag(self, interaction:discord.Interaction, user:discord.Member, reason:str='None Provided'):
        embed = discord.Embed(title='USER FLAGGED', description=f'{interaction.user.mention} Flagged {user.mention} for the following reason: \n`{reason}`', color=0xff0000)
        chan = interaction.guild.get_channel(1113149145671286804)
        await chan.send(embed=embed, content="<@&1113004706873212979>")
        await interaction.response.send_message('A message has been sent to the moderators, thanks for making this server safe!', ephemeral=True)

            
    