"""Music commands cog"""

from typing import cast
import discord
from discord.ext import commands
from discord.ext.commands import Context
import wavelink

from core.utils.checks import voice_check
from core.music.player import Player
from core.utils.regex import is_url


class Music(commands.Cog):
    """Music commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # join command
    @commands.hybrid_command(
        name="join",
        description="Join a voice channel.",
        aliases=["j", "connect"],
        usage="join",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=False)
    async def join(self, ctx: Context):
        if ctx.voice_client:
            player: Player = cast(Player, ctx.voice_client)
            if player.connected:
                return await ctx.send("I am already connected to a voice channel!", delete_after=10)
            else:
                player = await ctx.author.voice.channel.connect(cls=Player, self_deaf=True)
                player.text_channel = ctx.channel
                return await ctx.send(f"Joined {player.channel.mention}!")
        else:
            try:
                player = await ctx.author.voice.channel.connect(cls=Player, self_deaf=True)
                player.text_channel = ctx.channel
                return await ctx.send(f"Joined {player.channel.mention}!")
            except discord.ClientException:
                return await ctx.send("I am already connected to a voice channel!", delete_after=10)

    # leave command
    @commands.hybrid_command(
        name="leave",
        description="Leave the voice channel.",
        aliases=["disconnect", "dc"],
        usage="leave",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def leave(self, ctx: Context):
        player: Player = cast(Player, ctx.voice_client)
        if player.connected:
            await player.disconnect()
            return await ctx.send("Disconnected!")
        else:
            return await ctx.send("I am not connected to a voice channel!", delete_after=10)

    # play command
    @commands.hybrid_command(
        name="play",
        description="Play a song.",
        aliases=["p"],
        usage="play <song>",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def play(self, ctx: Context, *, query: str):
        player: Player = cast(Player, ctx.voice_client)

        if is_url(query):
            tracks: wavelink.Search = await wavelink.Playable.search(query)
        else:
            tracks: wavelink.Search = await wavelink.Pool.fetch_tracks(f"ytsearch:{query}")
        if not tracks:
            return await ctx.send("No tracks found!")

        player: Player
        try:
            player = await ctx.author.voice.channel.connect(cls=Player, self_deaf=True)
            player.text_channel = ctx.channel
        except discord.ClientException:
            player = cast(Player, ctx.voice_client)
            player.text_channel = ctx.channel
        except AttributeError:
            return await ctx.send(
                "I am not connected to a voice channel! Use the `join` command to connect to a voice channel.",
                delete_after=10,
            )
        
        if isinstance(tracks, wavelink.Playlist):
            added: int = await player.queue.put_wait(tracks)
            await ctx.send(f"Added {added} tracks from playlist `{tracks.name}` to the queue!")
            tracks.track_extras = [setattr(track, 'requester', ctx.author) for track in tracks.tracks]
        else:
            track: wavelink.Playable = tracks[0]
            await player.queue.put_wait(track)
            track.requester = ctx.author
            await ctx.send(f"Added **{track.title}** to the queue!")

        if not player.playing:
            await player.play(player.queue.get())
    
    @play.error
    async def play_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("Please provide a song to play!", delete_after=10)
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"You are on cooldown! Try again in {error.retry_after:.2f} seconds.", delete_after=10)
    
    # pause command
    @commands.hybrid_command(
        name="pause",
        description="Pause the current song.",
        usage="pause",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def pause(self, ctx: Context):
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return await ctx.send("I am not connected to a voice channel!", delete_after=10)
        
        if player.paused:
            return await ctx.send("The player is already paused!", delete_after=10)
        await player.set_pause(True)
        return await ctx.send("Paused!")
    
    @pause.error
    async def pause_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"You are on cooldown! Try again in {error.retry_after:.2f} seconds.", delete_after=10)
    

    # resume command
    @commands.hybrid_command(
        name="resume",
        description="Resume the current song.",
        usage="resume",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def resume(self, ctx: Context):
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return await ctx.send("I am not connected to a voice channel!", delete_after=10)
        
        if not player.paused:
            return await ctx.send("The player is already playing!", delete_after=10)
        await player.set_pause(False)
        return await ctx.send("Resumed!")
    
    @resume.error
    async def resume_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"You are on cooldown! Try again in {error.retry_after:.2f} seconds.", delete_after=10)
        
    # skip command
    @commands.hybrid_command(
        name="skip",
        description="Skip the current song.",
        aliases=["s"],
        usage="skip",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def skip(self, ctx: Context):
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return await ctx.send("I am not connected to a voice channel!", delete_after=10)
        
        if player.queue.empty():
            return await ctx.send("There are no tracks in the queue!", delete_after=10)
        await player.stop()
        return await ctx.send("Skipped!")
    
    @skip.error
    async def skip_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"You are on cooldown! Try again in {error.retry_after:.2f} seconds.", delete_after=10)
        
    
    # queue command
    @commands.hybrid_command(
        name="queue",
        description="Display the queue.",
        aliases=["q"],
        usage="queue",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def queue(self, ctx: Context):
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return await ctx.send("I am not connected to a voice channel!", delete_after=10)
        
        if player.queue.empty():
            return await ctx.send("There are no tracks in the queue!", delete_after=10)
        
        queue: str = "\n".join(
            f"{i + 1}. **{track.title}** - {track.requester.mention}"
            for i, track in enumerate(player.queue)
        )
        return await ctx.send(f"**Queue**:\n{queue}")
    
    @queue.error
    async def queue_error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"You are on cooldown! Try again in {error.retry_after:.2f} seconds.", delete_after=10)
        else:
            return await ctx.send("There was an error processing your request!", delete_after=10)
        
    
    # nowplaying command
    @commands.hybrid_command(
        name="nowplaying",
        description="Display the currently playing song.",
        aliases=["np"],
        usage="nowplaying",
        cooldown_after_parsing=True,
    )
    @commands.cooldown(1, 3, commands.BucketType.user)
    @voice_check(in_same_voice=True)
    async def nowplaying(self, ctx: Context):
        player: Player = cast(Player, ctx.voice_client)
        if not player:
            return await ctx.send("I am not connected to a voice channel!", delete_after=10)
        
        if not player.playing:
            return await ctx.send("There are no tracks playing!", delete_after=10)
        
        track: wavelink.Playable = player.current
        return await ctx.send(f"**Now Playing**: {track.title} - {track.requester.mention}")
    

async def setup(bot: commands.Bot):
    """Setup function for the cog."""
    await bot.add_cog(Music(bot))
