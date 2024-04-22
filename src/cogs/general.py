"""General commands cog"""

from discord.ext import commands


class General(commands.Cog):
    """General commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Shows bots latency",
        aliases=["pong"],
        usage="ping",
        cooldown_after_parsing=True,
    )
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.user)

    async def ping(self, ctx: commands.Context) -> None:
        """Check the bot's latency"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup(bot):
    """ Add the cog to the bot"""
    await bot.add_cog(General(bot))
