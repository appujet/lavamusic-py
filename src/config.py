""" Config file for the bot. """

import os
import discord
from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN = os.getenv('TOKEN')
    CLIENT_ID = os.getenv('CLIENT_ID')
    PREFIX = os.getenv('PREFIX')
    GUILD_ID = discord.Object(id=int(os.getenv('GUILD_ID')))
    # Music
    LAVALINK_URL = os.getenv('LAVALINK_URL')
    LAVALINK_AUTH = os.getenv('LAVALINK_AUTH')
    LAVALINK_NAME = os.getenv('LAVALINK_NAME')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
