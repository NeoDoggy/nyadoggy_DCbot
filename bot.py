import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
# import logging

# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
load_dotenv()
token=os.getenv('bot_token')

# command_prefix="/"
intents=discord.Intents.all()
# bot=commands.Bot(command_prefix=command_prefix,intents=intents,help_command=None)

class bot(commands.Bot):
    def __init__(self):
        self.bot=bot
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.all(),
            help_command=None
        )

    async def setup_hook(self):
        await self.load_extension('cogs.mainCog')
        await self.load_extension('cogs.helpCog')
        await self.load_extension('cogs.musicCog')
        await self.load_extension('cogs.animeStreamCog')




bot().run(token)