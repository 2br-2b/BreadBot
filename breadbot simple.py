from discord.ext import commands
import discord


emoji = '🍞'

# Create the bot
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("Started!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=emoji))
    
@bot.event
async def on_message(message):
    await message.add_reaction(emoji)

bot.run(os.environ['TOKEN'])
