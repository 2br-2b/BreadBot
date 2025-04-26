from discord.ext import commands
import discord
import json

# A Discord bot that reacts to every message with an emoji
# The bot should be controlled by any user in the list of admins
# The admins have the following commands:
#   !ignore <user> - Adds a user to the list of users to ignore. The users should be stored in preferences.json
#   !unignore <user> - Removes a user from the list of users to ignore. The users should be stored in preferences.json
#   !ignorec <channel> - Adds a channel to the list of channels to ignore. The channels should be stored in preferences.json
#   !unignorec <channel> - Removes a channel from the list of channels to ignore. The channels should be stored in preferences.json
#   !addadmin <user> - Adds a user to the list of admins. The admins should be stored in preferences.json
#   !removeadmin <user> - Removes a user from the list of admins. The admins should be stored in preferences.json
#   !setemoji <emoji> - Changes the emoji that the bot reacts with for a given server. The emoji per server should be stored in preferences.json. The default emoji is the bread emoji
#   !disable - Kills the bot
# The bot's token should be an environment variable
# The bot's prefix should be stored in preferences.json
# If the preferences.json file doesn't exist, create it with the default values
# When the bot is added to a server, it should react to every message with the default emoji. The bot should store an individual emoji for each different server in preferences.json

default_emoji = '🍞'

# Load the preferences.json file
preferences = {}
try:
    with open('preferences.json') as f:
        preferences = json.load(f)
except FileNotFoundError:
    preferences = {
        'prefix': '!',
        'admins': [],
        'ignored_users': [],
        'ignored_channels': [],
        'emoji_per_server': {}
    }
    with open('preferences.json', 'w') as f:
        json.dump(preferences, f)
        


# Load the bot's settings
token = os.environ['TOKEN']
prefix = preferences['prefix']
admins = preferences['admins']
ignored_users = preferences['ignored_users']
ignored_channels = preferences['ignored_channels']
emoji_per_server = preferences['emoji_per_server']


# Create the bot
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("Started!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" for messages"))
    
    
@bot.event
async def on_message(message):
    await bot.process_commands(message) 
    if message.author.bot:
        return
    if message.channel.id in ignored_channels:
        return
    if message.author.id in ignored_users:
        return
    if message.content.startswith(prefix):
        return
    if message.guild.id not in emoji_per_server:
        emoji_per_server[message.guild.id] = default_emoji
    await message.add_reaction(emoji_per_server[message.guild.id])


class AdminCommands (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ignore', help='Adds a user to the list of users to ignore', aliases=['iu'])
    async def ignore(self, ctx, user: discord.User):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the user is already ignored
        if user.id in ignored_users:
            await ctx.send('User is already ignored')
            return
        
        ignored_users.append(user.id)
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"{user.mention} has been added to the list of ignored users")
        
    @commands.command(name='unignore', help='Removes a user from the list of users to ignore', aliases=['uu'])
    async def unignore(self, ctx, user: discord.User):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the user is not ignored
        if user.id not in ignored_users:
            await ctx.send('User is not ignored')
            return
        
        ignored_users.remove(user.id)
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"{user.mention} has been removed from the list of ignored users")
        
        
    @commands.command(name='ignorec', help='Adds a channel to the list of channels to ignore', aliases=['ic', 'ignorechannel'])
    async def ignorec(self, ctx, channel: discord.TextChannel):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the channel is already ignored
        if channel.id in ignored_channels:
            await ctx.send('Channel is already ignored')
            return
        
        ignored_channels.append(channel.id)
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"{channel.mention} has been added to the list of ignored channels")
        
        
    @commands.command(name='unignorec', help='Removes a channel from the list of channels to ignore', aliases=['uc', 'unignorechannel'])
    async def unignorec(self, ctx, channel: discord.TextChannel):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the channel is not ignored
        if channel.id not in ignored_channels:
            await ctx.send('Channel is not ignored')
            return
        
        ignored_channels.remove(channel.id)
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"{channel.mention} has been removed from the list of ignored channels")
        
        
    @commands.command(name='setemoji', help='Sets the emoji to react to every message with', aliases=['changeemoji', 'emoji'])
    async def setemoji(self, ctx, emoji: str):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        emoji_per_server[ctx.guild.id] = emoji
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"Emoji has been set to {emoji}")
        
        
    @commands.command(name='setprefix', help='Sets the prefix to use for commands', aliases=['changeprefix', 'prefix', 'pf'])
    async def setprefix(self, ctx, prefix: str):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the prefix is not a single character
        if len(prefix) != 1:
            await ctx.send('Prefix must be a single character')
            return
        
        # Change the bot's prefix
        bot.command_prefix = prefix
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"Prefix has been set to {prefix}")
        
        
    @commands.command(name='setadmin', help='Adds a user to the list of admins', aliases=['op', 'addadmin'])
    async def setadmin(self, ctx, user: discord.User):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the user is already an admin
        if user.id in admins:
            await ctx.send('User is already an admin')
            return
        
        admins.append(user.id)
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"{user.mention} has been added to the list of admins")
        
        
    @commands.command(name='unsetadmin', help='Removes a user from the list of admins', aliases=['unop', 'removeadmin'])
    async def unsetadmin(self, ctx, user: discord.User):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Give an error if the user is not an admin
        if user.id not in admins:
            await ctx.send('User is not an admin')
            return
        
        admins.remove(user.id)
        with open('preferences.json', 'w') as f:
            json.dump({
                'prefix': prefix,
                'admins': admins,
                'ignored_users': ignored_users,
                'ignored_channels': ignored_channels,
                'emoji_per_server': emoji_per_server
            }, f)
        await ctx.send(f"{user.mention} has been removed from the list of admins")
        
        
    @commands.command(name='disable', help='Disables the bot', aliases=['stop', 'off', 'kill'])
    async def disable(self, ctx):
        # Make sure that the sender is an admin
        if ctx.author.id not in admins:
            return
        
        # Disable the bot
        await bot.close()

bot.add_cog(AdminCommands(bot))
bot.run(token)


