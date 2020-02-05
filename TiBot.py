import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl

from Lunch import lunch

from ShadowHunters import prepSH
from ShadowHunters import diceRoll
from ShadowHunters import clearPartie

TOKEN = ''

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context = True)
async def hello(ctx):
    await ctx.send('Hello {0.author.mention}'.format(ctx.message))
        
@bot.command(pass_context = True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    
    print(f"TiBot has connected to {channel}")
    await ctx.send(f"Connecté au salon {channel}")

@bot.command(pass_context = True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"TiBot has left {channel}")
        await ctx.send(f"Déconnecté des salons vocaux")
    else:
        print(f"TiBot was told to leave voice channel, but was not in one")
        await ctx.send(f"Je ne pense pas être dans un salon vocal actuellement")

@bot.command(pass_context = True)
async def midi(ctx):
    await ctx.send("Ce midi, pour les indécis, ce sera " + lunch() + ". Bon appétit !")

@bot.command(pass_context = True, aliases = ['sh'])
async def shadowhunters(ctx):
    try:
        voice = get(ctx.message.guild.channels, name = "Shadow Hunters")
        members = voice.members
        players = []
        for member in members:
            players.append(member.name)
        first = prepSH(players)
        
        for member in members:
            path = os.path.join('Partie', member.name+'.jpg')
            await member.send('Voici ton personnage pour Shadow Hunters :', file = discord.File(path))
            await member.send('Tu commences sur le lieu ' + str(diceRoll()) + '. Bon jeu !')
            os.remove(path)
        
        await ctx.send("Vous avez tous reçu votre rôle. C'est " + first + " qui commence ! Bon jeu :)")
    except:
        clearPartie()
        await ctx.send("Il y a un problème avec cette commande... Réessayez en vérifiant que le canal 'Shadow Hunters' existe toujours. Si cela ne fonctionne toujours pas, il va falloir aller debugger !")


bot.run(TOKEN)
