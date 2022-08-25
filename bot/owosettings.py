from database import update_record, query
from dictionaries import *
import discord, asyncio
from default import default_settings
from bot_essentials import user_input, error_message, invalid_role_input, unknown_error, timeout_message, timeout_length, is_guild_admin, not_enough_permissions

async def change_prefix(db, msg, client):
    if not is_guild_admin(db, msg.guild, msg.channel, msg.author):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    output = 'You may now enter the new prefix you want to change to.'
    colour = colours["blurple"]
    title = 'Changing prefix'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    await msg.channel.send(embed=embed)
    input = await user_input(msg, client)
    if input is None:
        return
    if input.content.find(' ') != -1 or input.content.find('\'') != -1:
        output = 'Invalid input, prefix entered has spaces, returning.'
        return
    input.content = '\'' + input.content + '\''
    try:
        update_record(db, msg.guild.id, 'prefix', input.content)
    except:
        await msg.channel.send(embed=unknown_error())
        return
    else:
        title = 'Prefix has successfully changed!'
        output = 'Your prefix has successfully changed to ' + input.content + '!'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    await msg.channel.send(embed=embed)
    return

async def get_prefix(db, msg, client):
    output = 'Your prefix is \'' + str(query(db, msg.guild.id, 'prefix')[0]) + '\''
    colour = colours["blurple"]
    title = 'Your prefix'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    await msg.channel.send(embed=embed)
    return

async def reset_prefix(db, msg, client):
    if not is_guild_admin(db, msg.guild, msg.channel, msg.author):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return

    output = 'Confirm resetting your prefix? (Enter yes/no)'
    colour = colours['purple']
    title = 'User confirmation'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    await msg.channel.send(embed=embed)
    input = await user_input(msg, client)
    if input is None:
        return
    if input.content.lower() == 'yes':
        tmp = '\'' + default_settings['prefix'] + '\''
        update_record(db, msg.guild.id, 'prefix', tmp)
        title = 'Action successful!'
        output = 'Your prefix has successfully been reset to ' + default_settings['prefix']
    else:
        title = 'Action unsuccessful.'
        output = 'Action has been stopped due to user termination'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    await msg.channel.send(embed=embed)

async def get_admin(db, msg, client):
    if not is_guild_admin(db, msg.guild, msg.channel, msg.author):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    rv = query(db, msg.guild.id, 'admin_roles')[0]
    title = 'List of admin roles'
    output = ''
    for role_id in list(map(int,rv.split())):
        output += msg.guild.get_role(role_id).mention + '\n'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['greyple'])
    await msg.channel.send(embed=embed)
    
async def add_admin(db, msg, client):
    if not is_guild_admin(db, msg.guild, msg.channel, msg.author):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    title = 'Addition of admin roles'
    output = 'Now, please mention the role in order to add them as an admin role.'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['greyple'])
    await msg.channel.send(embed=embed)
    try:
        input = await client.wait_for('message', timeout=timeout_length)
    except asyncio.exceptions.TimeoutError:
        await msg.channel.send(embed=timeout_message(msg))
        return
    else:
        if await invalid_role_input(input):
            return
        lst = query(db, msg.guild.id, 'admin_roles')[0].split()
        role = msg.guild.get_role(int(input.content[3:-1]))
        if str(role.id) in lst:
            output = 'This role is already an admin role.\nPlease try again.'
            embed = discord.Embed(title=error_message,type='rich',description=output,color=colours['greyple'])
            await msg.channel.send(embed=embed)
            return
        try:
            update_record(db, msg.guild.id, 'admin_roles', '\'' + query(db, msg.guild.id, 'admin_roles')[0] + ' ' + input.content[3:-1] + '\'')
        except:
            await msg.channel.send(embed=unknown_error())
            return
        else:
            title = 'Action successful!'
            output = role.mention + ' has been successfully added to the admin list'
            embed = discord.Embed(title=title,type='rich',description=output,colour=colours['greyple'])
            await msg.channel.send(embed=embed)
    
async def remove_admin(db, msg, client):
    if not is_guild_admin(db, msg.guild, msg.channel, msg.author):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    title = 'Addition of admin roles'
    output = 'Now, please mention the role in order to remove it from the admin list.'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['greyple'])
    await msg.channel.send(embed=embed)
    input = await user_input(msg, client)
    if input is None:
        return
    if await invalid_role_input(input):
        return
    role = msg.guild.get_role(int(input.content[3:-1]))
    lst = query(db, msg.guild.id, 'admin_roles')[0].split()
    if str(role.id) not in lst:
        output = 'This role is not an admin role.\nPlease try again.'
        embed = discord.Embed(title=error_message,type='rich',description=output,color=colours['greyple'])
        await msg.channel.send(embed=embed)
        return
    lst.remove(str(role.id))
    s = '\'' + ' '.join(lst) + '\''
    try:
        update_record(db, msg.guild.id, 'admin_roles', s)
    except:
        await msg.channel.send(embed=unknown_error())
        return
    else:
        title = 'Action successful!'
        output = role.mention + ' has been successfully removed from the admin list'
        embed = discord.Embed(title=title,type='rich',description=output,colour=colours['greyple'])
        await msg.channel.send(embed=embed)


    