import os
import random
import discord
from log import Log
from datetime import date, datetime, timedelta
from discord.ext import commands

logs = {}

timeout = 3
TOKEN = os.environ.get('NTcyMjg2OTkxMDMxNDY4MDM1.XMaGcQ.5oC4tjNbM29lau7MpuBRB6_CIWY')

bot = commands.Bot(command_prefix='!', description='A spam bot for Eric!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.change_presence(activity=discord.Game(name='Spamwatch v0.1'))

@bot.event
async def on_message(message):
    #ignore this bot's own messages
    if message.author == bot.user:
        return

    if message.author.name in logs:
        delta = message.created_at-logs[message.author.name].lastMessage
        if(delta.seconds < timeout):
            logs[message.author.name].violations += 1
            await message.delete()
            await message.channel.send('{0} Peringatan Spam!'.format(message.author))
        
        logs[message.author.name].lastMessage = message.created_at
    else:
        logs[message.author.name] = Log(message.created_at)

    # Since we have on_message, need to call the bot commands here
    await bot.process_commands(message)

@bot.command(pass_context=True)
async def ping(ctx):
    start = datetime.now()
    m = await ctx.send('Ping?')
    span = datetime.now()-start
    ms = span.microseconds/1000
    await m.edit(content='Pong! {0}ms'.format(ms))

@bot.command(pass_context=True)
async def spam(ctx):
    name = ctx.message.author.name
    if name in logs:
        log = logs[name]
        if log.violations > 0:
            await ctx.send('{0} Total  {1.violations} Pelanggaran .'.format(name, log))
        else:
            await ctx.send('{0} Tidak ada pelanggaran , Bagus!'.format(name))
    else:
        ctx.send('???')


@bot.command()
async def add(ctx, left : int, right : int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
async def threshold(ctx, span : int):
    timeout = span
    await ctx.send('Updated spam threshold to {0} seconds.'.format(timeout))

bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Protector", description="CAPSUL_FLY! :) List Perintah:", color=0xeee657)

    embed.add_field(name="!help", value="Detail Bot Protector", inline=False)
    embed.add_field(name="!ping", value="Cek Koneksi Bot", inline=False)
    embed.add_field(name="!spam", value="Cek Pelanggaran ", inline=False)
    #threshold hidden command

    await ctx.send(embed=embed)

# Run bot
bot.run(TOKEN)
