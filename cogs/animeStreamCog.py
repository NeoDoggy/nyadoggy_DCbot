import discord
from discord.ext import commands,tasks
from discord import app_commands
import random
import yt_dlp
import asyncio
import json
import websockets
from pprint import pprint

opts={
    "quiet":    True,
    "simulate": True,
    "forceurl": True,
}

colors = [  0xf94144, 
            0xf3722c, 
            0xf8961e, 
            0xf9844a, 
            0xf9c74f, 
            0x90be6d, 
            0x43aa8b, 
            0x4d908e, 
            0x577590, 
            0x277da1, 
         ]

class animeStreamCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.is_playing = False
        self.music_queue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""
        self.nowplaying = {}

    async def send_ws(self, ws, data):
        json_data = json.dumps(data)
        await ws.send(json_data)

    async def send_pings(self, ws, interval=45):
        while True:
            await asyncio.sleep(interval)
            msg = { 'op': 9 }
            await self.send_ws(ws, msg)

    @tasks.loop(seconds=1.0)
    async def getplaylist(self):
        url = 'wss://listen.moe/gateway_v2'
        ws = await websockets.connect(url)
        while True:
            data = json.loads(await ws.recv())
            if data['op'] == 0:
                heartbeat = data['d']['heartbeat'] / 1000
                self.bot.loop.create_task(self.send_pings(ws, heartbeat))
            elif data['op'] == 1:
                self.nowplaying=data


    async def play_music(self,guild):
        if len(self.music_queue) > 0:
            self.is_playing = True
            self.vc=discord.utils.get(self.bot.voice_clients,guild=guild)
            if self.vc == "" or self.vc == None or not self.vc.is_connected() :
                self.vc = await self.music_queue[0][1].connect()
            else:
                try:
                    await self.vc.disconnect()
                    self.vc = await self.music_queue[0][1].connect()
                except:
                    await self.vc.move_to(self.music_queue[0][1])
            # print(self.music_queue)
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=None)
        else:
            self.is_playing = False

    async def play_anime(self,guild):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
            self.vc=discord.utils.get(self.bot.voice_clients,guild=guild)
            if self.vc == "" or self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()
            else:
                try:
                    await self.vc.disconnect()
                    self.vc = await self.music_queue[0][1].connect()
                except:
                    await self.vc.move_to(self.music_queue[0][1])
            # print(self.music_queue)
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_music(guild), self.bot.loop))
        else:
            self.is_playing = False
    
    @app_commands.command(name="streamanime", description="play an anime song string")
    async def playAnimeStream(self, interaction: discord.Interaction):
        try:
            voice_channel = interaction.user.voice.channel
        except:
            await interaction.response.send_message("Not in a voice channel")
            return
        await interaction.response.send_message("playing animeStream")
        self.music_queue.append(["https://listen.moe/stream", voice_channel, "listen.moe", "NULL", "NULL", "NULL"])#http://curiosity.shoutca.st:8019/stream
        if self.is_playing == False:
            await self.play_anime(guild=interaction.guild)
    
    @app_commands.command(name="endstream", description="Disconnecting bot from VC")
    async def leaveAnime(self, interaction: discord.Interaction):
        await interaction.response.send_message("leaved")
        self.music_queue.clear()
        try:
            await self.vc.disconnect()
        except:
            self.vc=discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
            await self.vc.disconnect()

    @app_commands.command(name="nowstream", description="Now playing on stream")
    async def nowStream(self, interaction: discord.Interaction):
        try:
            eM=discord.Embed(   title=f"{discord.PartialEmoji(name='gooby_wiggle',animated=True,id=1228386715052544040)}  Now Playing  {discord.PartialEmoji(name='gooby_wiggle',animated=True,id=1228386715052544040)}",
                                color=random.choice(colors)).add_field(
                                name = f"{self.nowplaying['d']['song']['title']}", value= f"\n**artist**: {self.nowplaying['d']['song']['artists'][0]['name']}\n**album**: {self.nowplaying['d']['song']['albums'][0]['name']}\n**startTime**: {self.nowplaying['d']['startTime']}\n**dur**: {self.nowplaying['d']['song']['duration']}\n\n", inline = False).set_footer(
                                text="listen.moe",
                                icon_url='https://i.imgur.com/6I7XW0M.png').set_thumbnail(url=f"https://cdn.listen.moe/covers/{self.nowplaying['d']['song']['albums'][0]['image']}")
            await interaction.response.send_message(embed=eM,ephemeral=False)
        except:
            try:
                eM=discord.Embed(   title=f"{discord.PartialEmoji(name='gooby_wiggle',animated=True,id=1228386715052544040)}  Now Playing  {discord.PartialEmoji(name='gooby_wiggle',animated=True,id=1228386715052544040)}",
                                color=random.choice(colors)).add_field(
                                name = f"{self.nowplaying['d']['song']['title']}", value= f"\n**artist**: {self.nowplaying['d']['song']['artists'][0]['name']}\n**startTime**: {self.nowplaying['d']['startTime']}\n**dur**: {self.nowplaying['d']['song']['duration']}\n\n", inline = False).set_footer(
                                text="listen.moe",
                                icon_url='https://i.imgur.com/6I7XW0M.png')
                await interaction.response.send_message(embed=eM,ephemeral=False)
            except:
                em=discord.Embed(title=f"{self.bot.get_emoji(958768110247223296)} Error!!!", description=f"Currently not streaming", color=0xff4060) 
                await interaction.response.send_message(embed=em,ephemeral=True)

    async def cog_load(self):
        self.getplaylist.start()
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        self.getplaylist.stop()
        print(f"{self.__class__.__name__} unloaded!")

async def setup(bot):
    await bot.add_cog(animeStreamCog(bot))