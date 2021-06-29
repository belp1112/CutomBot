import random
from discord.ext import commands
import discord
intents = discord.Intents.all()  #全てのIntentsオブジェクトを生成
intents.typing = False
client = commands.Bot(intents=intents,command_prefix = '$')

def create_member_list(ctx):
    return ctx.author.voice.channel.members


async def random_split_team(ctx, member_list):
    shuffled = random.sample(member_list, len(member_list))
    team_a = shuffled[:1]
    team_b = shuffled[1:]
    reply_msg = '以下のチームになりました\n'
    reply_msg += '```Aチーム\n'
    for member in team_a:
        reply_msg += f'・{member.name}\n'
    reply_msg += 'Bチーム\n'
    for member in team_b:
        reply_msg += f'・{member.name}\n'
    reply_msg += '```\n'
    reply_msg += 'チームを確定して移動なら`yes`再選なら`no`を入力してください'
    await ctx.reply(reply_msg)
    return team_b