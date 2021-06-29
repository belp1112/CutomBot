async def move_to(ctx):
    channel = ctx.author.guild.get_channel(752138086087000084)
    await ctx.author.move_to(channel, reason='for test')

for i in range(5):
    idx = f'{i + 1} {i}'
    print(idx)