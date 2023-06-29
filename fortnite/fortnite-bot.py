import discord
from discord.ext import commands

import fortnite_api
from fortnite_api.enums import GameLanguage

api = fortnite_api.FortniteAPI("YOUR-KEY")

languages = {
'ar': 'ARABIC',
'en': 'ENGLISH',
'de': 'GERMAN',
'es': 'SPANISH',
'es-419': 'SPANISH_LATIN',
'fr': 'FRENCH',
'it': 'ITALIAN',
'ja': 'JAPANESE',
'ko': 'KOREAN',
'pl': 'POLISH',
'pt-BR': 'PORTUGUESE_BRASIL',
'ru': 'RUSSIAN',
'tr': 'TURKISH',
'zh-CN': 'CHINESE_SIMPLIFIED',
'zh-Hant': 'CHINESE_TRADITIONAL'
}

# Add a function after declare fortnite-api
def iter_obj(req_class):
    """Iterate over an object and print each attribute"""
    for variable in dir(req_class):
        if not variable.startswith('__'):
            #yield ("{}: {}".format(variable, getattr(req_class, variable))) too much large longitude raises a discord exception
            print("{}: {}".format(variable, getattr(req_class, variable)))
            
            
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

@bot.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

@bot.command()
async def cosmetics(ctx, lang: str, *, name: str):
    """Shows info about cosmetics, given his name and search language"""
    try:
        cosmetic = api.cosmetics.search_all(search_language=getattr(GameLanguage, languages[lang]), name=name)
        embeds = []
        for c in cosmetic:
            embed = discord.Embed()
            embed.title = c.name
            embed.description = c.description
            embed.set_image(url=c.icon.url)
            embed.set_footer(text=c.introduction_text, icon_url=c.small_icon.url)
            embeds.append(embed)
        await ctx.send(embeds=embeds)
    except fortnite_api.errors.NotFound as e:
        await ctx.send("Please enter a valid name")
        await ctx.send(e)
        
@bot.command()
async def player(ctx, *, name: str):
    """Returns player stats data such as overall, duo, solo, trio, and others..."""
    try:
        player = api.stats.fetch_by_name(name)
        player = player.stats.all
        embeds = {}
        for var in dir(player):
            if not var.startswith('__') and var != 'raw_data':
                embed = discord.Embed()
                s = ""
                nested_obj = getattr(player, var)
                for variable in dir(nested_obj):
                    if not variable.startswith('__'):
                        s += "{}: {}".format(variable, getattr(nested_obj, variable))
                        s += '\n'
                embed.title = var
                embed.description = s
                embed.set_footer(text="Player: %s" % (name))
                embeds[var] = embed
        await ctx.send(embeds=[embeds[key] for key in embeds.keys()])
    except fortnite_api.errors.NotFound as e:
        await ctx.send("Incorrect player name")
        await ctx.send(e)
        
bot.run('YOUR-TOKEN')
