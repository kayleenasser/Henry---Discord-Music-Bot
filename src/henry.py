# Kaylee's epic music bot for discord
# Plays music on discord voice chat via youtube
from tokenbot import bot_token
import discord
import youtube_dl
from discord.ext import commands  # Imports discord commands

client = commands.Bot(command_prefix='!')  # !command to call on command
client.remove_command('help')  # Removes help command so I can use my own

FFMPEG_OPTIONS = {
    'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}  # FFMEPG options
YDL_OPTIONS = {'format': "bestaudio"}  # Youtube download options
queue_list = []  # keep track of queue music
is_playing = False  # determine if music is playing


# STARTUP FUNCTIONS:
# -------------------------------------------
# Search Youtube Function
# Gathers link from youtube to be used
def yt_search(url):
    global YDL_OPTIONS
    global FFMPEG_OPTIONS
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(
                "ytsearch:%s" % url, download=False)['entries'][
                0]  # Gathers youtube video info based off link or search
        except Exception:
            return False  # If it cant download the info
    return {
        'source': info['formats'][0]['url'],
        'title': info['title']
    }  # Formats the downloaded link


# Next Function
# Will play the next song in the queue and continue until the queue is empty using a recursive function
def next(vc):
    global is_playing
    global queue_list
    global FFMPEG_OPTIONS
    if len(queue_list) > 0:
        is_playing = True

        # Get the first url
        m_url = queue_list[0][0]['source']

        # Remove first element in the queue as its currently playing
        queue_list.pop(0)

        vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS),
                after=lambda e: next(vc))

    else:
        is_playing = False


# Loop check
async def play_music(vc):
    global is_playing
    global queue_list
    global YDL_OPTIONS
    global FFMPEG_OPTIONS
    if len(queue_list) > 0:
        is_playing = True

        m_url = queue_list[0][0]['source']
        print(queue_list)  # Tells me whats in the queue

        # Remove the first element in the queue as its currently playing
        queue_list.pop(0)

        vc.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS),
                after=lambda e: next(vc))
    else:
        is_playing = False


# Start-up (Join/Disconnect)
# ---------------------------------------
@client.event  # Tells me if this is running in the console
async def on_ready():
    print('The epic bot is online B)')


@client.command(pass_context=True, aliases=['j'])  # Join VC
async def join(ctx):
    if ctx.author.voice:  # Joins VC with user
        await ctx.send("Hello! (•◡•) /")
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Join a VC first silly!")  # User needs to enter VC


@client.command(pass_context=True, aliases=['d'])  # Disconnect from VC
async def disconnect(ctx):
    await ctx.send("Goodbye! ʕ•́ᴥ•̀ʔっ")
    await ctx.voice_client.disconnect()


# Help
@client.command(pass_context=True, aliases=['h'])  # help commands
async def help(ctx):
    await ctx.send(
        'Commands:\n!join or !j- bot joins your channel, you must do this to use the music functions\n\n!playnow or '
        '!pn *insert youtube link or search term* - plays immediately\n\n!queue or !q or p! *insert youtube link or '
        'search term* - adds to queue\n\n!view or !v - view queue \n\n!skip or !sk- skips to next song in '
        'queue\n\n!remove or !rmv # - remove whatever song numbered in queue is by checking !view\n\n!clear or !c - '
        'clears queue\n\n!pause or !ps - pauses song\n\n!resume or !r - resumes playing song\n\n!stop or !s - stops '
        'song from playing \n\n!disconnect or !d- disconnects bot from channel '
    )


@client.command(pass_context=True)  # Introduction to bot
async def intro(ctx):
    await ctx.send("Hi there! I'm henry the music bot! Type !help or !h for instructions on how to use me!  ٩(＾◡＾)۶")


@client.command(pass_context=True) # Kill program - brings bot offline
async def kill(ctx):
    await ctx.send("Looks like you've killed me! No longer running")
    await client.logout()
    print("Henry is offline!")


# ------------------------
# Run Program: 
# ------------------------
client.run(bot_token)
