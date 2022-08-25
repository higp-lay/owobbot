import discord, sqlite3
from dotenv import load_dotenv, dotenv_values
from bot_essentials import get_prefix_of_message, get_command_of_message
from database import query, connect_database, create_table
from default import *
from dictionaries import *
from commands import *

client = discord.Client()
db = connect_database()

@client.event
async def on_ready():
    print('We have logged in as {}'.format(str(client.user)))

@client.event
async def on_guild_join(guild):
    # print('a')
    if query(db, guild.id, 'id') is not None:
        embed = discord.Embed(title='owob bot',type='rich',description=already_in_database,colour=colours["dark_red"])
    else:
        set_starter_default(db, guild.id)
        embed = discord.Embed(title='owob bot',type='rich',description=start_message,colour=colours["gold"])
    await guild.system_channel.send(embed=embed)

@client.event
async def on_message(message):
    msg = message
    msg.content = msg.content.lower()
    print(msg.content)
    prefix = query(db, msg.guild.id, 'prefix')[0]
    # print()
    if message.author == client.user:
        return
    else:
        try:
            if get_prefix_of_message(msg.content, prefix) == prefix:
                cmd = get_command_of_message(msg.content, prefix)
                # print(cmd)
                try:
                    await globals()[cmd](db, msg, client)
                except KeyError:
                    output = 'There is no command called \'' + cmd + '\'\nPlease try again.\nYou may refer to the command list by running \'' + prefix + ' help\''
                    embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
                    await msg.channel.send(embed=embed)
            elif client.user.mentioned_in(msg):
                await hi(db, msg, client)
        except:
            pass
            
        
TOKEN = dotenv_values(".env")['TOKEN']
client.run(TOKEN)