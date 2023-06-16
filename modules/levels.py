from .database import LevelsDatabase
import discord
from discord.ext import commands
from discord import app_commands
import time
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



options = webdriver.ChromeOptions()
options.add_argument("--headless")
wd = webdriver.Chrome(options=options)


class Levels(commands.Cog):
    
    @app_commands.command()
    async def createtable(self, interaction:discord.Interaction):
        if interaction.user.id != 729873770990534766: return  await interaction.response.send_message('You cant edit the database')
        LevelsDatabase.createTable()
        await interaction.response.send_message('Created Table!')
        
    @app_commands.command()
    async def deletetable(self, interaction:discord.Interaction):
        if interaction.user.id != 729873770990534766: return await interaction.response.send_message('You cant edit the database')
        LevelsDatabase.DeleteTable()
        await interaction.response.send_message('Deleted Database')
    
    
    @app_commands.command(description='See the level of yourself or any other user')
    @app_commands.describe(
        user = 'the user you want to see the level of'
    )
    async def level(self, interaction:discord.Interaction, user:discord.Member=None, hidden:bool=True):
        if user == None: user = interaction.user
        record = LevelsDatabase.getRecord('level, xp', user.id)
        level = record[0]
        xp = record[1]
        base = level*100
        embed = discord.Embed(title=f"{user.name}'s Level", description=f"Level: `{level}`\nXP: `{xp}`\n XP til next level: `{base}`", color=0x00ff00)
        await interaction.response.send_message(embed=embed, ephemeral=hidden)
        
    
    @app_commands.command(description='Set the level of yourself or any other user')
    @app_commands.describe(
        user = 'the user you want to see the level of'
    )
    async def setlevel(self, interaction:discord.Interaction, user:discord.Member, level:int):
        if interaction.user.guild_permissions.administrator == False: await interaction.response.send_message('You can\'t edit levels', ephemeral=True); return
        date = math.floor(time.time())
        LevelsDatabase.CreateRecord(user.id, level, 0, date)
        await interaction.response.send_message(f'I have set {user.mention}\'s level to: {level}')
        
        
    
    @app_commands.command()
    async def test(self, interaction:discord.Interaction):
        wd.get('base.html')
        wd.save_screenshot('idk.png')
        await interaction.response.send_message('I did it..?')
    
    @commands.Cog.listener('on_message')
    async def on_message(self, msg:discord.Message):
        if msg.author.bot == True: return
        else: user = msg.author
        data = LevelsDatabase.getRecord(data="*", userid=user.id)
        if data == None:
            date = math.floor(time.time())
            LevelsDatabase.CreateRecord(user.id, 1, 0, date)
            return
        level = data[1]
        xp = data[2]
        date = data[3]
        base = level *100
        #check if its been 60 seconds since last message
        curtime = math.floor(time.time()) 
        if curtime - date <=15: return
        print(f"Writing xp for {user}")
        xp+=15
        if xp >=base:
            level+=1
            xp = math.floor(xp%base)
            await msg.channel.send(f"CONGRATS {user.mention}! You just leveled up! Level: {level}")
            
        LevelsDatabase.CreateRecord(user.id, level, xp, curtime)
   
    @app_commands.command(description='Claim the rewards of yourself, or claim the rewards for another user')
    async def claim_rewards(self, interaction:discord.Interaction, user:discord.Member=None):
        if not user: user = interaction.user
        level = LevelsDatabase.getRecord('level', user.id)[0]
        if level >= 15:
            level15 = interaction.guild.get_role(1116156383574892614)
            await user.add_roles(level15)
            embed = discord.Embed(title='Rewards claimed!', description=f'I have given {user.mention} the following rewards:\n{level15.mention}', color=0x0000ff)
            await interaction.response.send_message(embed=embed, content=user.mention)
        else:
            await interaction.response.send_message(f'{user.mention}\'s level isnt high enough!\nLevel needed: 15\nLevel: {level}')
            
            
            
        
        
    
        