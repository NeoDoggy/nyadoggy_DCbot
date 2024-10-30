import discord
from discord.ext import commands
from discord import app_commands

class mainCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Delete Message',
            callback=self.deleteMessage,
        )
        self.bot.tree.add_command(self.ctx_menu)

    @commands.Cog.listener()
    async def on_ready(self):
        slash = await self.bot.tree.sync()
        for i in slash:
            print(i)
        print(f'loaded {len(slash)} commands')
        # activity = discord.Game(name="/help for commands")
        activity = discord.CustomActivity(f'🗣 /help for commands!',emoji=discord.PartialEmoji(name="oooooh",animated=True,id=869447774876336139))
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        print(f'{self.bot.user} is ready to work')

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error): 
        if isinstance(error, commands.CommandNotFound): 
            em = discord.Embed(title=f"{self.bot.get_emoji(958768110247223296)} Error!!!", description=f"Command not found.\nuse /help for commands", color=0xff4060) 
            await ctx.send(embed=em)
        else:
            print(error)

    @commands.command(name="pping")
    async def pingcmd(self, ctx):
        await ctx.send('pong')

    @app_commands.command(name="weeeee", description="BoooobeeeeBiiiird")
    async def weeeeee(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.bot.get_emoji(869447774876336139),delete_after=3)

    async def deleteMessage(self, interaction: discord.Interaction, message: discord.Message):
        if(message.author.id==self.bot.application_id):
            await message.delete()
            await interaction.response.send_message(f"Message deleted",ephemeral=True)
        else:
            em = discord.Embed(title=f"{self.bot.get_emoji(958768110247223296)} Error!!!", description=f"Message not sent by me!!", color=0xff4060).set_image(url="https://i.imgur.com/gYUapTq.gif") 
            await interaction.response.send_message(embed=em,ephemeral=True)


        # await interaction.response.send_message(msg)
#---------------------------------REMOVE WHEN PRODUCTED---------------------------------#
    # @commands.command(name="load")
    # async def load(self,ctx,extension):
    #     await self.bot.load_extension(f"cogs.{extension}")
    #     await ctx.send(f"Loaded {extension} done.")
    
    # @commands.command(name="unload")
    # async def unload(self,ctx,extension):
    #     await self.bot.unload_extension(f"cogs.{extension}")
    #     await ctx.send(f"UnLoaded {extension} done.")

    @commands.command(name="reload")
    async def reload(self,ctx,extension):
        await self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"Reloaded {extension} done.")
#---------------------------------REMOVE WHEN PRODUCTED---------------------------------#

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

async def setup(bot):
    await bot.add_cog(mainCog(bot))