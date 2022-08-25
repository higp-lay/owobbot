import discord
from dictionaries import colours
from dotenv import dotenv_values
from default import length_of_id

error_message = 'An error has occured!'
timeout_length = 15.0
owner_id = dotenv_values(".env")['author_id']

def get_prefix_of_message(s, p):
    if len(s.split()[0]) == len(p):
        return s.split()[0]
    else:
        return s[:len(p)]

def get_command_of_message(s, p):
    if len(s.split()[0]) == len(p):
        if len(s.split()) == 1:
            return 'hi'
        return s.split()[1]
    else:
        return s[len(p):]

def unknown_error():
    title = 'An unknown error has occured'
    output = 'I\'m sorry if this happens, but please try again later!'
    colour = colours['red']
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    return embed

def timeout_message(msg):
    output = 'Timed out!'
    colour = colours['red']
    embed = discord.Embed(title=error_message,type='rich',description=output,colour=colour)
    return embed

async def invalid_role_input(msg):
    if msg.content == '@everyone':
        output = msg.content + ' role is not available to be modified at the moment.\nPlease try again later.'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return True

    if msg.content[:3] != '<@&' or msg.content[-1] != '>':
        output = 'You are not mentioning a role.\nPlease try again!'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return True
    role = msg.guild.get_role(int(msg.content[3:-1]))
    if role is None:
        output = 'This role does not exist!\nPlease try again!'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return True

async def is_invalid_user(msg, id, client):
    try:
        user = await client.fetch_user(user_id=int(id))
        return user
    except ValueError:
        tmp = id
        id = id.replace('<@!','')
        id = id.replace('<@','')
        id = id.replace('>','')
        if not id.isnumeric():
            output = tmp + ' is not a valid user, try again!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
            await msg.channel.send(embed=embed)
            return None
        try:
            user = await client.fetch_user(user_id=int(id))
            return user
        except discord.NotFound:
            output = tmp + ' does not exist.\nPlease try again!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
            await msg.channel.send(embed=embed)
            return None
        except discord.HTTPException:
            output = 'Discord API error.\nPlease try again later!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
            await msg.channel.send(embed=embed)
            return None
    except discord.NotFound:
        output = tmp + ' does not exist.\nPlease try again!'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return None
    except discord.HTTPException:
        output = 'Discord API error.\nPlease try again later!'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return None
    

def is_bot_owner(msg):
    return str(msg.author.id) == owner_id

# def is_member_in_perm_list(msg, lst):

def not_enough_permissions(msg):
    output = 'You do not have enough permission to run this command.'
    embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
    # await msg.channel.send(embed=embed)
    return embed

def is_guild_admin(db, guild, channel, guild_member):
    from database import query
    lst = query(db, guild.id, 'admin_roles')[0].split()
    if channel.permissions_for(guild_member).administrator:
        return True
    else:
        for role in guild_member.roles:
            if str(role.id) in lst:
                return True
        return False

def has_permissions(db, msg, lst):
    if is_guild_admin(db, msg.guild, msg.channel, msg.author):
        return True
    for permission in lst:
        attribute = getattr(msg.channel.permissions_for(msg.author),permission)
        if not attribute:
            return False
    return True

async def user_input(msg, client):
    import asyncio
    try:
        def check(m):
            return m.author == msg.author
        input = await client.wait_for('message', check=check, timeout=timeout_length)
    except asyncio.exceptions.TimeoutError:
        await msg.channel.send(embed=timeout_message(msg))
        return None
    else:
        return input
    
async def check_if_int(msg):
    try:
        msg = int(msg.content)
    except ValueError:
        output = msg.content + ' is not an integer.\nPlease try again.'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return None
    else:
        return msg
    
async def try_bot_action(msg, action):
    try:
        return action
    except discord.Forbidden:
        output = 'owobbot does not have enough permission to execute this action.\nPlease contact your server administrator to resolve this issue by granting the related permission to owobbot.'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return False
    except discord.HTTPException:
        output = 'Discord API error.\nPlease try again later!'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return False
    

def is_in_guild(user, guild):
    return guild.get_member(user.id) is not None
