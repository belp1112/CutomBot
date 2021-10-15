import random
from discord.ext import commands
import discord
intents = discord.Intents.all()  #全てのIntentsオブジェクトを生成
intents.typing = False


def create_member_list(ctx):
    return ctx.author.voice.channel.members


async def random_split_team(ctx, member_list):
    shuffled = random.sample(member_list, len(member_list))
    team_a = shuffled[:1]
    team_b = shuffled[1:]
    reply_msg = 'Members have splited as right down below\n'
    reply_msg += '```A team\n'
    for member in team_a:
        reply_msg += f'・{member.name}\n'
    reply_msg += 'B team\n'
    for member in team_b:
        reply_msg += f'・{member.name}\n'
    reply_msg += '```\n'
    reply_msg += 'Confirm and move members to VC channel `yes`\n'
    reply_msg += 'Make team again `no`'
    await ctx.reply(reply_msg)
    return team_a, team_b


def check_1(m):
    return m.content == 'yes' or m.content == 'no'


async def wait_for_yesno(ctx, member_list, team_b, client):
    msg = await client.wait_for('message', check=check_1, timeout=None)
    if msg.content == 'yes':
        channel = ctx.guild.get_channel(865162272741785620)#チーム１チャンネルID
        for member in team_b:
            await member.move_to(channel, reason='have fun')
        await msg.author.reply('Members has been moved')
        return
    elif msg.content == 'no':
        await random_split_team(ctx, member_list)
        await wait_for_yesno(ctx, member_list,team_b,client)


async def wait_for_uncount_member(ctx, member_list, reply_msg_over10, client):
    await ctx.reply(reply_msg_over10)
    msg = await client.wait_for('message',check=check_2, timeout=None)
    new_member_list = []
    new_member_list.extend(member_list)
    split_msg = msg.content.split(' ')
    reply_msg_uncount_confirm = '```'
    from_zero = 0
    for i in split_msg:
        from_zero += 1
        reply_msg_uncount_confirm += f'{from_zero}:{member_list[int(i)-1].name}\n'
    reply_msg_uncount_confirm += '```'
    reply_msg_uncount_confirm += 'Are you sure to split team without these member?\n`yes` or `no`'
    await msg.reply(reply_msg_uncount_confirm)
    msg2 = await client.wait_for('message',check=check_1,timeout=None)
    if msg2.content == 'yes':
        for i in split_msg:
            del new_member_list[int(i)-1]
            if len(new_member_list) == 10:
                return new_member_list
            else:
                msg2.reply('Member is less then 10 people')
                wait_for_uncount_member(ctx, member_list,reply_msg_over10,client)


    elif msg2.content == 'no':
        await wait_for_uncount_member(ctx, member_list, reply_msg_over10, client)


def check_2(m):
    split_m = m.content.split(' ')
    try:
        for i in split_m:
            int(i)
        return True
    except ValueError:
        return False