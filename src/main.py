""" Main file to run the bot """

import asyncio
import logging
import os

import discord
import wavelink
from discord.ext import commands
from config import Config


class Bot(commands.Bot):
    """Bot class"""

    def __init__(self) -> None:
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents: discord.Intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        discord.utils.setup_logging(level=logging.INFO)
        super().__init__(
            command_prefix=commands.when_mentioned_or(Config.PREFIX), intents=intents, allowed_mentions=allowed_mentions
        )

    async def setup_hook(self) -> None:
        """Setup hook for the bot"""

        nodes = [
            wavelink.Node(
                uri=Config.LAVALINK_URL,
                password=Config.LAVALINK_AUTH,
                identifier=Config.LAVALINK_NAME,
            )
        ]

        await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100)
        self.tree.copy_global_to(guild=Config.GUILD_ID)
        await self.tree.sync(guild=Config.GUILD_ID)

    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload) -> None:
        """When the wavelink node is ready"""
        logging.info("Wavelink Node connected. ID: %s", payload.node.identifier)

    async def load_extensions(self) -> None:
        """Load all extensions"""
        cogs_length: int = 0
        for filename in os.listdir("src/cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    cogs_length += 1
                except ImportError as e:
                    logging.error("Failed to load extension %s\n%s", filename[:-3], e)
        logging.info("Loaded %s cogs", cogs_length)

        events_length: int = 0
        for filename in os.listdir("src/listeners"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"listeners.{filename[:-3]}")
                    events_length += 1
                except ImportError as e:
                    logging.error("Failed to load extension %s\n%s", filename[:-3], e)
        logging.info("Loaded %s Listeners", events_length)


bot = Bot()


async def main() -> None:
    """Main function to run the bot"""
    async with bot:
        await bot.login(Config.TOKEN)
        await bot.load_extensions()
        await bot.connect()


asyncio.run(main())
