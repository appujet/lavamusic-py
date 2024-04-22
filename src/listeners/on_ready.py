import discord
from discord.ext import commands
import logging

class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Logged in as %s (%s)", self.bot.user, self.bot.user.id)
        
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"Beta | {len(self.bot.guilds)} servers",
            ),
            status=discord.Status.online,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(OnReady(bot))
