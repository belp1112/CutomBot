import discord
from discord import message
from discord.ext import commands
import os
from functions import create_member_list, random_split_team, wait_for_yesno, wait_for_uncount_member


TOKEN = os.getenv('CustomGameBot')
intents = discord.Intents.all()  #全てのIntentsオブジェクトを生成
intents.typing = False
client = commands.Bot(intents=intents, command_prefix = '$')


@client.event
async def on_ready():
    print('$$Bot is online$$')


@client.command()
async def ready(ctx):
    if ctx.author.bot:
        return

    member_list = create_member_list(ctx)


    if len(member_list) == 10:#10人の場合
        team_b = await random_split_team(ctx, member_list)
        await wait_for_yesno(ctx, member_list, team_b, client)


    elif len(member_list) >= 11:#11人以上の場合
        reply_msg_over10 = '```'
        for i in range(len(member_list)):
            reply_msg_over10 += f'{i+1}:{member_list[i].name}\n'
        reply_msg_over10 += '```\n'
        reply_msg_over10 += 'Enter the nombers of member who not join the Game with space'
        new_member_list = await wait_for_uncount_member(ctx,member_list,reply_msg_over10,client)
        team_b = await random_split_team(ctx,new_member_list)
        await wait_for_yesno(ctx,new_member_list,team_b,client)


    elif len(member_list) <= 9:#9人以下の場合
        await ctx.reply(f'Members are not enough。(Currently {len(member_list)} people)')


@client.command()
async def back(ctx):
    ovject_channel = client.get_channel(837295798114189336)
    target_channel = client.get_channel(844918521631866950)
    members = target_channel.members
    for i in members:
        pass
client.run(TOKEN)