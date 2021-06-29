import discord
from discord.ext import commands
import os
from functions import create_member_list, random_split_team


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
        async def wait_for(ctx, member_list, team_b):
            msg = await client.wait_for('message', check=check, timeout=None)
            if msg.content == 'yes':
                channel = ctx.guild.get_channel(844918521631866950)#かきぴ家ニートチャンネルID
                for member in team_b:
                    await member.move_to(channel, reason='have fun')
                await msg.author.reply('メンバー移動しました')
                return
            elif msg.content == 'no':
                await random_split_team(ctx, member_list)
                await wait_for(ctx, member_list,team_b)
        await wait_for(ctx, member_list, team_b)

    elif len(member_list) >= 3:#11人以上の場合
        added_num_member = []
        for i in member_list:
            added_num_member.append[[len(range(member_list))]:[i.name]]
        reply_msg_over10 = '```'
        for i in added_num_member:
            reply_msg_over10 += f'{i}\n'
        reply_msg_over10 += '```'
        ctx.reply(reply_msg_over10)    

    
    elif len(member_list) <= 2:#9人以下の場合
        await ctx.reply(f'人数が足りません。(現在{len(member_list)}人です)')


@client.command()
async def id(ctx):
    member_data = ctx.author.voice.channel.members
    await ctx.channel.send(member_data)


def check(m):
    return m.content == 'yes' or m.content == 'no'



client.run(TOKEN)