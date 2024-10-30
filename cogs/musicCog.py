import discord
from discord.ext import commands
from discord import app_commands
import random
import yt_dlp
import asyncio

opts={
    "quiet":    True,
    "simulate": True,
    "forceurl": True,
}

class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.is_playing = False
        self.music_queue = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = ""

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False

    async def play_music(self,guild):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
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
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False
    
    @app_commands.command(name="play", description="play ytmusic with url")
    @app_commands.describe(link="input youtube link")
    async def play(self, interaction: discord.Interaction, link:str):
        try:
            voice_channel = interaction.user.voice.channel
        except:
            await interaction.response.send_message("Not in a voice channel")
            return
        songRaw=""
        songUrl=""
        songTitle=""
        songTbnail=""
        songDur=""
        songAuthor=""
        if(link.startswith("https://www.youtube.com/")==False and link.startswith("https://youtu.be/")==False and link.startswith("https://m.youtube.com/")==False):
            em=discord.Embed(title=f"{self.bot.get_emoji(958768110247223296)} Error!!!", description=f"Not a vaild youtube link", color=0xff4060) 
            await interaction.response.send_message(embed=em)
            return
        with yt_dlp.YoutubeDL(opts) as ytdl:
            songRaw=ytdl.extract_info(link,download=False)
            songUrl=songRaw['formats'][6]['url']
            songTitle=songRaw['title']
            songTbnail=songRaw['thumbnail']
            songDur=songRaw['duration_string']
            songAuthor=songRaw['uploader']
        if type(songUrl)==type(True):
            await interaction.response.send_message("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
        else:
            eMa=discord.Embed(title=f"{discord.PartialEmoji(name='outline_check_ani',animated=True,id=1228386729984004116)}  Succuessfully added song to queue",color=0x00BA7C).add_field(
                            name = f'{songTitle}', 
                            value= f"""\n
                                by {songAuthor}
                                duration: {songDur}s
                                \n""", 
                                inline = False).set_footer(
                                text="music commands > play",
                                icon_url='https://i.imgur.com/jtBJhrQ.jpg').set_thumbnail(
                                url=songTbnail
                            )
            await interaction.response.send_message(embed=eMa)
            self.music_queue.append([songUrl, voice_channel, songTitle, songTbnail, songAuthor, songDur])
            if self.is_playing == False:
                await self.play_music(guild=interaction.guild)

    @app_commands.command(name="queue", description="Displays the current songs in queue")
    async def queue(self, interaction: discord.Interaction):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"{i}. {self.music_queue[i][2]} by {self.music_queue[i][4]}-{self.music_queue[i][5]}\n"
        print(retval)
        if retval != "":
            await interaction.response.send_message(retval)
        else:
            await interaction.response.send_message("No music in queue")
    
    @app_commands.command(name="skip", description="Skips the current song being played")
    async def skip(self, interaction: discord.Interaction):
        if(len(self.music_queue)==0):
            await interaction.response.send_message("queue is empty")
            return
        if self.vc != "" and self.vc:
            self.vc.stop()
            await interaction.response.send_message("skipped music")
            await self.play_music(guild=interaction.guild)
    
    @app_commands.command(name="leave", description="Disconnecting bot from VC")
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.send_message("leaved")
        self.music_queue.clear()
        try:
            await self.vc.disconnect()
        except:
            self.vc=discord.utils.get(self.bot.voice_clients,guild=interaction.guild)
            await self.vc.disconnect()

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(bot):
    await bot.add_cog(musicCog(bot))