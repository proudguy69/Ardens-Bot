import discord
from discord.ext import commands
import json

# modules
from modules.moderation import Moderation
from modules.levels import Levels
from modules.tickets import Tickets, ticketSelView

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=discord.Intents.all())
        
    async def setup_hook(self):
        print(f"{self.user} is starting~!")
        await self.add_cog(Moderation())
        await self.add_cog(Levels())
        await self.add_cog(Tickets(self))
        await self.add_view(ticketSelView())

bot = Bot()
file = open('settings.json', 'r')
settings = json.load(file)
tree = bot.tree



#context menus

@tree.context_menu(name='Flag Message')
async def flag_message(interaction:discord.Interaction, message:discord.Message):
    embed = discord.Embed(title='🏳️MESSAGE FLAGGED🏳️', description=f'{interaction.user.mention}({interaction.user}) Flagged {message.author.mention}({message.author})\'s message: `{message.content}`\n\nRaw Message: \"{message.content}\"\n\n Link: {message.jump_url}', color=0xff0000)
    chan = interaction.guild.get_channel(1113149145671286804)
    await message.add_reaction('🏳️')
    await chan.send(embed=embed, content="<@&1113004706873212979>")
    await interaction.response.send_message('I have notified staff!', ephemeral=True)





@bot.command()
async def sync(c):
    await c.send('Syncing Server..')
    await tree.sync()
    await c.send('Finished Syncing!')
@sync.error
async def syncerr(ctx, error):
    await ctx.send(error)
    





bot.run(settings['token'])