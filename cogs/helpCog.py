import discord
from discord.ext import commands
from discord import app_commands
import random

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

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Music",emoji="🎵",description="Music commands"),
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    async def callback(self, interaction: discord.Interaction):
        # if self.values[0] == "twitter":
        #     await interaction.response.edit_message(content="choosed twitter")
        # elif self.values[0] == "Birdee":
        #     await interaction.response.send_message(birdeeEmoji,ephemeral=False)
        # elif self.values[0] == "hentai":
        #     await interaction.response.send_message("no echi",ephemeral=True)
        if self.values[0] == "Music":
            eM=discord.Embed(title=f"{discord.PartialEmoji(name='music_ani',animated=True,id=1228389685873610914)}  Music  {discord.PartialEmoji(name='music_ani',animated=True,id=1228389685873610914)}",color=random.choice(colors)).add_field(
                            name = 'commands:', value= "\n**/play** `youtube url` - play youtube videos\n\n**/queue** - show music queue\n\n**/skip** - skip, as shown\n\n**/leave** - also, as shown\n\n", inline = False).set_footer(
                            text="help center > music commands",icon_url='https://i.imgur.com/jtBJhrQ.jpg')
            await interaction.response.send_message(embed=eM,ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class helpCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.test="haha"

    @app_commands.command(name="help", description="wow, a command list")
    async def help(self, interaction: discord.Interaction):
        eh=discord.Embed(title=":exclamation:| Help",description="choose a help label below",color=random.choice(colors))
        await interaction.response.send_message(embed=eh,view=SelectView(),ephemeral=True)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(bot):
    await bot.add_cog(helpCog(bot))