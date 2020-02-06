import discord
from discord.ext import commands
from discord.utils import get
import os
import youtube_dl

from Lunch import lunch

from ShadowHunters import prepSH
from ShadowHunters import diceRoll
from ShadowHunters import clearPartie


TOKEN = ""

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send("Hello {0.author.mention}".format(ctx.message))

@bot.command(pass_context=True)
async def join(ctx):
    global voice
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        voice = get(bot.voice_clients, guild = ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        print(f"TiBot has connected to {channel}")
        await ctx.send(f"Connecté au salon {channel}")
    else:
        await ctx.send("Tu n'es dans aucun salon vocal")

@bot.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        if voice.is_playing():
            stop(ctx)
        await voice.disconnect()
        print(f"TiBot has left {channel}")
        await ctx.send("Déconnecté des salons vocaux")
    else:
        print("TiBot was told to leave voice channel, but was not in one")
        await ctx.send("Je ne pense pas être dans un salon vocal")

@bot.command(pass_context=True)
async def play(ctx, url: str):
    try:
        if os.path.isfile("song.mp3"):
            os.remove("song.mp3")
            print("Removed song.mp3")
    except PermissionError:
        print("Trying to delete song file being played")
        await ctx.send("Une musique est déjà jouée actuellement")
        return

    await ctx.send("Préparation de la lecture...")

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now...")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            os.rename(file, "song.mp3")
            print(f"Renamed File: {file}")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), 
               after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    new_name = name.rsplit("-", 2)
    new_name = "%s - %s" % (new_name[0], new_name[1])
    print("Audio playing")
    await ctx.send(f"Lecture de {new_name} en cours")

@bot.command(pass_context=True)
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        print("Audio paused")
        await ctx.send("Musique mise en pause")
    else:
        print("TiBot was told to pause audio, but none is playing")
        await ctx.send("Aucune musique en cours")

@bot.command(pass_context=True)
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        print("Audio resumed")
        await ctx.send("Reprise de la musique")
    else:
        print("TiBot was told to resume audio, but none is paused")
        await ctx.send("Aucune musique en pause")

@bot.command(pass_context=True)
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        print("Audio stopped")
        await ctx.send("Musique arrêtée")
    else:
        print("TiBot was told to stop audio, but none is playing")
        await ctx.send("Aucune musique en cours")

@bot.command(pass_context=True)
async def midi(ctx):
    print("TiBot decided what to eat at lunch")
    await ctx.send("Ce midi, pour les indécis, ce sera %s. Bon appétit !" 
                   % lunch())

@bot.command(pass_context=True, aliases=['sh'])
async def shadowhunters(ctx):
    try:
        voice = get(ctx.message.guild.channels, name = "Shadow Hunters")
        members = voice.members
        players = []
        for member in members:
            players.append(member.name)
        first = prepSH(players)

        for member in members:
            path = os.path.join("Partie", member.name+".jpg")
            await member.send("Voici ton personnage pour Shadow Hunters :", file=discord.File(path))
            await member.send("Tu commences sur le lieu %s. Bon jeu !" % str(diceRoll()))
            os.remove(path)

        await ctx.send("Vous avez tous reçu votre rôle. C'est %s qui commence. Bon jeu !" % (first))
    except:
        clearPartie()
        await ctx.send("Il y a un problème avec cette commande... Vérifiez que le canal 'Shadow Hunters' existe toujours et qu'il y a au moins une personne dedans. Si cela ne fonctionne toujours pas, il va falloir aller debugger !")


bot.run(TOKEN)
