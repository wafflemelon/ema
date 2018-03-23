#!/usr/bin/env python3

"""This extension sets the bot's playing status."""

import discord


def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_ready")
    async def when_ready():
        """Conduct preparations once the bot is ready to go."""

        name = f"Ema help | {bot.config['version']} |"
        game = discord.Game(name=f"{name} [{str(bot.shard_count)}]")

        await bot.change_presence(status=discord.Status.online, activity=game)
