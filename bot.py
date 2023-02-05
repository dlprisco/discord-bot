import discord
from discord.ext import commands
import random
import os
from coinmarketcapapi import CoinMarketCapAPI

cmc = CoinMarketCapAPI('4d9d9591-bba7-4c45-9db1-25ce9d62a69c')

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def available(ctx):
    """Simplified & refactored per server response"""
    rep = cmc.cryptocurrency_listings_latest()
    await ctx.send("\n".join(['> ' + str(i+1) + '. '+ rep.data[i]['symbol'] for i in range(len(rep.data))]))
    
@bot.command()
async def status(ctx):
    try:
        rep = cmc.cryptocurrency_info(symbol=symbol)
    except Exception:
        await ctx.send('You need to specify a correct symbol')
        return
        
    embed = discord.Embed()
    embed.set_image(url = rep.data[symbol][0]['logo'])
  
    ll = cmc.cryptocurrency_listings_latest()
    price = -1
    for i in range(len(ll.data)):
        if ll.data[i]['symbol'] == symbol:
            price = ll.data[i]['quote']['USD']
    await ctx.send('> Description:\n```' + rep.data[symbol][0]['description'] + '```\n'+ ' Name:  `' + rep.data[symbol][0]['name'] + '\n' + ' price:  `$' + str(price['price']) + '`\n\nLogo\n', embed = embed)

@bot.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run('token')
