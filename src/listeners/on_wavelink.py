""" This module contains the on_wavelink event listener. """

import discord
from discord.ext import commands
import wavelink

from core.music.player import Player
from core.utils.format import FormatUtils


class OnWavelink(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload) -> None:
        format = FormatUtils()
        player: Player = payload.player
        original: wavelink.Playable | None = payload.original
        track: wavelink.Playable = player.current

        if not player:
            # Handle edge cases...
            return
        if not player.text_channel:
            return
        channel: discord.TextChannel = player.text_channel
        if not channel:
            return

        if not hasattr(track, "requester"):
            track.requester = self.bot.user

        embed = discord.Embed(
            title="Now Playing",
            description=f"[{track.title}]({track.uri})",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=track.artwork)

        embed.add_field(name="Duration", value=format.format_time(track.length), inline=True)

        if original and original.recommended:
            embed.description += f"\n\n`This track was recommended via {track.source}`"

        embed.set_footer(text=f"Requested by {track.requester.global_name}")

        player.last_message = await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnWavelink(bot))
