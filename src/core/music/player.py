"""This module contains a custom player class that extends the Wavelink Player class."""

import discord
import wavelink as Wavelink


class Player(Wavelink.Player):
    """A custom player class that extends the Wavelink Player class."""

    text_channel: discord.TextChannel
    last_message: discord.Message
    autoplay: Wavelink.AutoPlayMode
    mode: Wavelink.QueueMode
    history: list[Wavelink.Playable]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_channel = None
        self.last_message = None
        self.autoplay = Wavelink.AutoPlayMode.disabled
        self.mode = Wavelink.QueueMode.normal
        self.history = []
   
    async def istop(self, force: bool = False):
        """Stops the player and clears the queue."""
        if self.autoplay == Wavelink.AutoPlayMode.enabled:
            self.autoplay = Wavelink.AutoPlayMode.disabled
        if self.queue.mode != Wavelink.QueueMode.normal:
            self.queue.mode = Wavelink.QueueMode.normal
        self.queue.clear()
        await super().stop(force=force)


    def loop(self, mode: Wavelink.QueueMode):
        """Sets the loop mode for the player.
        Parameters
        ----------
        mode : QueueMode
            The mode to set the loop to.
        """
        self.queue.mode = mode

    