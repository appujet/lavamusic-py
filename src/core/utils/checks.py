"""This module contains custom checks for the bot."""
import discord
from discord.ext import commands
from discord.ext.commands import Context

def voice_check(in_voice: bool = True, in_same_voice: bool = False):
    """A custom check to ensure that the author is in a voice channel.

    Parameters
    ----------
    in_voice : bool
        Whether the author must be in a voice channel.
    in_same_voice : bool
        Whether the author must be in the same voice channel as the bot.

    Returns
    -------
    commands.check
        A check function that can be used with the `commands.check` decorator.
    """
    
    async def predicate(ctx: Context):
        if in_voice:
            if ctx.author.voice is None:
                voice_channels = [c.id for c in ctx.guild.channels if c.type == discord.ChannelType.voice]
                raise commands.CheckFailure(
                    f"You have to be connected to a voice channel on this server to use this command! \n\n How to join a voice channel? Just click on a channel with a speaker icon (for example, click here: {ctx.guild.get_channel(voice_channels[0]).mention}) [See the official Discord guide](https://support.discord.com/hc/en-us/articles/360045138571-Beginner-s-Guide-to-Discord#h_9de92bc2-3bca-459f-8efd-e1e2739ca4f4) for more information."
                )
        if in_same_voice:
            if ctx.voice_client:
                if ctx.author.voice.channel != ctx.voice_client.channel:
                    voice_channel: discord.VoiceChannel = ctx.voice_client.channel
                    raise commands.CheckFailure(
                        f"You must be in the same voice channel as me! \n\n You are currently in: {ctx.author.voice.channel.mention} \n I am currently in: {voice_channel.mention}"
                    )
        return True

    return commands.check(predicate)
