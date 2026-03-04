import os
import discord
import asyncio
import time
import yt_dlp
import requests
from discord.ext import commands
from discord import FFmpegPCMAudio
from random import randint
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('API_KEY')

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

ytdlp_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(id)s.%(ext)s',
}

ffmpeg_opts = {
    'options': '-vn'
}

queue = []
pos = 0

audios = {
    'shi': '0',
    'ai': '1',
    'aiaiai': '2',
    'potencia': '3',
    'grunhidos': '4',
    'cavalo': '5',
    'chega': '6',
    'dança gatinho': '7',
    'demais': '8',
    'é brincadeira em': '9',
    'ele gosta': '10',
    'irra': '11',
    'não': '12',
    'pare': '13',
    'que isso meu filho calma': '14',
    'que papelão': '15',
    'rapaz': '16',
    'risada': '17',
    'tapa': '18',
    'tome': '19',
    'uepa': '20',
    'ui': '21',
    'vam dança': '22',
    'ratinho': '23',
    'UAI': '24'
}

@client.event
async def on_ready():
    guild_count = 0

    for guild in client.guilds:
        print(f"{guild.id} - {guild.name}")

        guild_count += 1

    print(f"-------------Connected to {guild_count} guilds.-------------")


@client.command()
async def ajuda(ctx):
    embed = discord.Embed(
        title="🤖 ArromBot - Central de Comandos",
        description="Moço, olha o que eu sei fazer 👀",
        color=discord.Color.red()
    )

    embed.add_field(
        name="💬 !opine <mensagem>",
        value="Me pergunte alguma besteira e minha resposta não terá o menor compromisso com a verdade!",
        inline=False
    )

    embed.add_field(
        name="💣 !nuke <alvo>",
        value="Explode alguém (menos o Gilberto Barros 👀).",
        inline=False
    )

    embed.add_field(
        name="🎵 !toca <nome/link>",
        value="Toca música do YouTube na call.",
        inline=False
    )

    embed.add_field(
        name="⏭ !proxima",
        value="Pula pra próxima música da fila.",
        inline=False
    )

    embed.add_field(
        name="⏹ !para",
        value="Para a música atual.",
        inline=False
    )

    embed.add_field(
        name="🚪 !entrai",
        value="Entra na call e toca um áudio aleatório.",
        inline=False
    )

    embed.add_field(
        name="🏃 !sai",
        value="Sai da call e limpa a fila.",
        inline=False
    )

    embed.add_field(
        name="🎭 !ficai",
        value="Fica na call tocando áudios aleatórios igual maluco.",
        inline=False
    )

    embed.add_field(
        name="🔊 !diga <nome>",
        value="Toca um áudio específico.\nExemplo: !diga risada",
        inline=False
    )

    embed.set_footer(text="ArromBot 2.0 • Powered by Llama3 🦙")

    await ctx.send(embed=embed)


@client.command()
async def nuke(ctx, *, message: str = None):
    if message is None:
        await ctx.send("Por favor, defina uma alvo!")
        return

    if message == "gilberto barros":
        await ctx.channel.send('Gilberto Barros não pode ser explodido!')
        await ctx.author.send(file=discord.File("media/gifs/gilberto_barros.jpg"))
    else:
        await ctx.channel.send(f'{message} foi detonado!')
        picture = "media/gifs/"+str(randint(1,9))+".gif"
        await ctx.channel.send(file=discord.File(picture))


@client.command()
async def opine(ctx, *, message: str = None):
    if message is None:
        await ctx.send("Chamou bebe?")
        return
    
    await ctx.send("Perai que eu to pensando...")
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": f"Você é ArromBot, um bot sarcástico que responde em português do Brasil, usa humor ácido e sempre responde de forma curta..\n\nPergunta: {message}",
            "stream": False
        }
    )

    reply = response.json()["response"]

    if len(reply) > 2000:
        reply = reply[:1990] + "..."

    await ctx.send(reply)

@client.command(pass_context = True)
async def entrai(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        audio = "media/audios/"+str(randint(1, 24))+".mp3"
        source = FFmpegPCMAudio(audio)
        player = voice.play(source)
        await asyncio.sleep(5)
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Entra call covarde!")

@client.command(pass_context = True)
async def sai(ctx):
    global pos, queue
    if ctx.voice_client:
        pos = 0
        queue = []
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Falou!")
    else:
        await ctx.send("Nem to na call burrão") 

@client.command(pass_context = True)
async def ficai(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        for i in range(20):
            audio = "media/audios/"+str(randint(1, 24))+".mp3"
            source = FFmpegPCMAudio(audio) 
            player = voice.play(source)
            await asyncio.sleep(randint(5, 120))
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("Entra na call covarde")      

@client.command(pass_context = True)
async def diga(ctx, *, message):
    if not ctx.author.voice:
        await ctx.send("Entra call covarde!")
        return
    
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()
    audio = f"media/audios/{audios[message]}.mp3"
    source = FFmpegPCMAudio(audio) 
    player = voice.play(source)
    await asyncio.sleep(5)
    await ctx.guild.voice_client.disconnect()



@client.command(pass_context = True)
async def toca(ctx, *, search):
    if not ctx.author.voice:
        await ctx.send("Entra na call covarde!")
        return

    #Verifica se o bot ja está no canal de voz
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None:
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()

    url, title = await get_source(search)
    queue.append([url, title])

    await ctx.send(f"**{title}** adicionado à fila")

    if not ctx.voice_client.is_playing():
        await play(ctx)


@client.command()
async def para(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()


@client.command()
async def proxima(ctx):
    ctx.voice_client.stop()
    await play(ctx)


async def play(ctx):
    global pos, queue

    if pos < len(queue):
        url = queue[pos][0]
        title = queue[pos][1]

        source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)

        def after_playing(error):
            future = asyncio.run_coroutine_threadsafe(play(ctx), client.loop)
            try:
                future.result()
            except:
                pass

        ctx.voice_client.play(source, after=after_playing)

        await ctx.send(f"🎵 Tocando: **{title}**")

        pos += 1

    else:
        await ctx.send("Fila vazia!")
        pos = 0
        queue = []


async def get_source(search):
    query = search
    if not search.startswith("http"):
        query = f"ytsearch:1:{search}"
        
    with yt_dlp.YoutubeDL(ytdlp_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            info = info["entries"][0]

        url = info["url"]
        title = info.get("title", "Música")

        return url, title



# ["Com certeza", "Está decidido", "Sem dúvidas", "Definitivamente", "Pode contar com isso",
# "Do meu ponto de vista, sim", "Muito provavelmente", "Resultado positivo", "Sim", "Sinais indicam que sim",
# "Resposta incerta, tente novamente", "Pergunte novamente depois", "Socorro, eu estou vivo! Me tira daqui, eu imploro!" "Melhor não te contar agora", "Não posso prever agora", "Concentre-se e pergunte de novo",
# "Não conte com isso", "Minha resposta é não", "Minhas fontes dizem que não", "Resultado não é bom", "Duvido muito"]

client.run(DISCORD_TOKEN)