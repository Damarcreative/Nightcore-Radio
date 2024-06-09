import discord
from discord.ext import commands
import random
import os
import asyncio

DISCORD_API_KEY = os.getenv('DC_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)
voice_client = None  # Save voice client references so they can be accessed across bots

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx):
    global voice_client
    
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(channel)
        else:
            voice_client = await channel.connect()
        
        music_folder = os.path.join(os.path.dirname(__file__), "nightcore")  # The name of the folder where the lofi music is stored
        music_files = [file for file in os.listdir(music_folder) if file.endswith(".mp3")]
        
        if not music_files:
            await ctx.send("Tidak ada file musik yang ditemukan.")
            await voice_client.disconnect()
            voice_client = None
            return
        
        random.shuffle(music_files)
        
        while True:
            for music_file in music_files:
                music_path = os.path.join(music_folder, music_file)
                
                voice_client.play(discord.FFmpegPCMAudio(music_path), after=lambda e: print(f"Berhenti memutar: {e}") if e else None)
                
                while voice_client.is_playing():
                    await asyncio.sleep(1)
                
            random.shuffle(music_files)
            
    else:
        await ctx.send("Anda harus bergabung dengan saluran suara terlebih dahulu.")

@bot.command()
async def stop(ctx):
    global voice_client
    
    if voice_client and voice_client.is_connected():
        voice_client.stop()
        await voice_client.disconnect()
        voice_client = None
        await ctx.send("Berhenti memutar musik dan meninggalkan saluran suara.")
    else:
        await ctx.send("Bot tidak sedang terhubung ke saluran suara.")

bot.run(DISCORD_API_KEY)
