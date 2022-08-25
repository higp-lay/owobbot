import discord, asyncio, os
from bot_essentials import user_input, not_enough_permissions, is_bot_owner, timeout_message, timeout_length, error_message
from dictionaries import * 
from owosettings import *
from database import query

async def cal(db, msg,client):
    # output = 'Please enter a valid expression:'
    output = 'This command is still in development.'
    title = 'owob bot calculator'
    colour = colours["blue"]
    embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    embed.set_author(name=msg.author)
    await msg.channel.send(embed=embed)
    # answer = ''
    # try:
    #     input = await client.wait_for('message', timeout=timeout)
    # except (asyncio.exceptions.TimeoutError):
    #     colour = colours['red']
    #     answer = 'Timed out.'
    # else:
    #     expression = input.content
    #     try:
    #         for key in cal_replacements:
    #             # print(key, cal_replacements[key], sep = ' ')
    #             expression = expression.replace(key,cal_replacements[key])
    #         # print(expression)
    #         # DONT USE EVAL, I WILL IMPLEMENT STACKS (PERHAPS NEVER) TO CALCULATE EXPRESSIONS (sigh)
    #         answer = 'The answer of ' + input.content + ' is ' + str(eval(expression))
    #     except ZeroDivisionError:
    #         colour = colours['red']
    #         answer = input.content + ' is undefined'
    #     except:
    #         colour = colours['red']
    #         answer = input.content + ' is an invalid expression'
    # embed = discord.Embed(title=title,type='rich',description=answer,colour=colour)
    # await msg.channel.send(embed=embed)

async def help(db, msg, client):
    p = query(db, msg.guild.id, 'prefix')[0]
    # print(os.getcwd())
    os.chdir('help')
    if len(msg.content.split()) >= 3:
        command_being_searched = msg.content.split()[2]
    else:
        lines = 'The prefix of the bot in this server is ```' + p + '```\n'
        command_being_searched = 'general'
    try:
        # lines = '```' + command_being_searched
        lines = ''
        with open('{}.txt'.format(command_being_searched)) as f:
            lst = f.readlines()
            title = lst[0]
            lines += ''.join(lst[1:])
            f.close()
    except FileNotFoundError:
        title = 'Command not found!'
        lines = 'The command \'' + p + ' ' + command_being_searched + '\' does not exist! Please run \'' + p + ' help\' for command list.'
    os.chdir('..')
    colour = colours['gold']
    embed = discord.Embed(title=title,type='rich',description=lines,colour=colour)
    await msg.channel.send(embed=embed)
    
async def settings(db, msg, client):
    p = query(db, msg.guild.id, 'prefix')[0]
    lines = ''
    colour = colours["blurple"]
    os.chdir('help')
    with open('owosettings.txt') as f:
        lst = f.readlines()
        title = lst[0]
        lines += ''.join(lst[1:])
        f.close()
    os.chdir('..')
    embed = discord.Embed(title=title,type='rich',description=lines,colour=colour)
    await msg.channel.send(embed=embed)
    input = await user_input(msg, client)
    if input is None:
        return
    try:
        await globals()[input.content.lower()](db, msg, client)
    except KeyError:
        output = 'Invalid input \'' + input.content + '\'\n' + 'Please try again.\nYou may refer to the options by running \'' + p + ' help settings\''
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return
            
    # embed = discord.Embed(title=title,type='rich',description=output,colour=colour)
    
async def hi(db, msg, client):
    title = 'Greetings'
    output = 'Hi, how are you?\nThe prefix of owobbot using in this server is \'' + query(db, msg.guild.id, 'prefix')[0] + '\'.'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['green'])
    await msg.channel.send(embed=embed)

async def test(db, msg, client):
    if not is_bot_owner(msg):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    title = 'Hi'
    output = 'a'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['green'])
    await msg.channel.send(embed=embed)

async def ping(db, msg, client):
    import time
    title = 'Testing the Ping...'
    output = 'Please wait a while!'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['magenta'])
    start_time = time.time()
    await msg.channel.send(embed=embed)
    end_time = time.time()
    title = 'Ping Test done!'
    output = 'Bot latency = {}ms\nAPI latency = {}ms'.format(round(client.latency*1000,2),round((end_time-start_time)*1000,2))
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['magenta'])
    await msg.channel.send(embed=embed)

async def stop(db, msg, client):
    if not is_bot_owner(msg):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    else:
        title = 'Terminating the program...'
        output = 'Please wait a while...'
        embed = discord.Embed(title=title,type='rich',description=output,colour=colours['magenta'])
        await msg.channel.send(embed=embed)
        db.close()
        exit()

# async def spotify(db, msg, client):
#     title = 'owob Spotify!'
#     output = 'Please refer to the command list and enter the command that you want to run.'
#     embed = discord.Embed(title=title,type='rich',description=output,colour=colours['green'])
#     await msg.channel.send(embed=embed)
#     try:
#         input = await client.wait_for('message', timeout=timeout_length)
#     except asyncio.exceptions.TimeoutError:
#         await msg.channel.send(embed=timeout_message(msg))
#         return
#     else:
#         try:
#             globals()[input.content.lower()](db, msg, client)
#         except KeyError:
#             output = 'Invalid input \'' + input.content + '\'\n' + 'Please try again.\nYou may refer to the command list by running \'' + query(db, msg.guild.id, 'prefix')[0] + ' help spotify\''
#             embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
#             await msg.channel.send(embed=embed)
#             return

async def ban(db, msg, client):
    from bot_essentials import is_invalid_user, has_permissions, check_if_int, try_bot_action
    if not has_permissions(db, msg, ['ban_members']):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    output = 'You now have ' + str(timeout_length) + ' seconds to mention the user(s) that you want to ban, separated with spaces.'
    title = 'Ban hammer!'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['red'])
    await msg.channel.send(embed=embed)
    input = await user_input(msg, client)
    # print(input.content)
    if input is None:
        return
    lst = input.content.split()
    available_bans = []
    for ban in lst:
        user = await is_invalid_user(input, ban, client)
        if user is None:
            continue
        try:
            guild_member = await try_bot_action(msg, await msg.guild.fetch_member(user.id))
        except discord.NotFound:
            output = 'This user is not in the server.\nPlease try again!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
            await msg.channel.send(embed=embed)
            return False
        # print(guild_member)
        # if error
        if not guild_member:
            continue
        elif guild_member is None:
            output = user.mention + ' is not in the server.\nTry again!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
            await msg.channel.send(embed=embed)
        elif is_guild_admin(db, msg.guild, msg.channel, guild_member):
            output = 'You cannot ban a server admin ' + user.mention + '\nTry again!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
            await msg.channel.send(embed=embed)
        else:
            available_bans.append(guild_member)
    if not available_bans:
        output = 'No user is available to ban.\nPlease try again!'
        embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['red'])
        await msg.channel.send(embed=embed)
        return
    users_getting_banned = ', '.join(user.mention for user in available_bans)
    output = 'You now have ' + str(timeout_length) + ' seconds to enter the number of days worth of messages to delete from ' + users_getting_banned + '\nIt should be an integer and is from 0 to 7 (inclusive)'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['red'])
    await msg.channel.send(embed=embed)
    delete_message_days = await check_if_int(await user_input(msg, client))
    if delete_message_days is None:
        return
    output = 'You now have ' + str(timeout_length) + ' seconds to enter the reason to ban ' + users_getting_banned + '\nOr you can type \'none\' to leave it blank.'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['red'])
    await msg.channel.send(embed=embed)
    reason = await user_input(msg, client)
    tmp = reason
    tmp.content.lower()
    if reason is None:
        return
    elif tmp == 'none':
        reason = None
    else:
        reason = reason.content
    banned = []
    for user in available_bans:
        if not await try_bot_action(msg, await msg.guild.ban(user=user,reason=reason,delete_message_days=delete_message_days)):
            banned.append(user)
    if not banned:
        title = 'Unsucessful ban hammer!'
        output = 'No users were banned with the ban hammer.'
    else:
        banned_str = ', '.join([user.mention for user in banned])
        output = 'You have successfully banned ' + banned_str + ' for ' + ('no reason' if reason is None else reason)
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['red'])
    await msg.channel.send(embed=embed)

    
async def unban(db, msg, client):
    from bot_essentials import is_invalid_user, has_permissions, try_bot_action
    if not has_permissions(db, msg, ['ban_members']):
        await msg.channel.send(embed=not_enough_permissions(msg))
        return
    output = 'You now have ' + str(timeout_length) + ' seconds to provide the user id that you want to unban.'
    title = 'Unban hammer!'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['green'])
    await msg.channel.send(embed=embed)
    input = await user_input(msg, client)
    # await msg.channel.send(input.content)
    if input is None:
        return
    lst = input.content.split()
    available_unbans = []
    ban_lst = [ban.user.id for ban in await try_bot_action(msg, await msg.guild.bans())]
    if ban_lst is None:
        return
    for unban in lst:
        user = await is_invalid_user(input, unban, client)
        if user is None:
            continue
        if user.id not in ban_lst:
            output = user.mention + ' is not banned!\nPlease try again!'
            embed = discord.Embed(title=error_message,type='rich',description=output,colour=colours['green'])
            await msg.channel.send(embed=embed)
            continue
        else:
            available_unbans.append(user)
    users_getting_unbanned = ', '.join([user.name for user in available_unbans])
    output = 'You now have ' + str(timeout_length) + ' seconds to enter the reason to unban ' + users_getting_unbanned + '\nOr you can type \'none\' to leave it blank.'
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['green'])
    await msg.channel.send(embed=embed)
    reason = await user_input(msg, client)
    tmp = reason
    tmp.content.lower()
    print(tmp.content)
    if reason is None:
        return
    elif tmp == 'none':
        reason = None
    else:
        reason = reason.content
    unbanned = []
    for user in available_unbans:
        if not await try_bot_action(msg, await msg.guild.unban(user=user,reason=reason)):
            unbanned.append(user)
    if not unbanned:
        title = 'Unsucessful unban hammer!'
        output = 'No users were unbanned with the unban hammer.'
    else:
        unbanned_str = ', '.join([user.mention for user in unbanned])
        output = 'You have successfully unbanned ' + unbanned_str + ' for ' + ('no reason' if reason is None else reason)
    embed = discord.Embed(title=title,type='rich',description=output,colour=colours['green'])
    await msg.channel.send(embed=embed)
    return
