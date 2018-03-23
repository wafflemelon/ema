#!/usr/bin/env python3

"""Halt and restart commands."""

import sys
import os
import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


class Process:
    """Commands that affect the bot's running process."""

    @commands.command(aliases=["shutdown", "kys"])
    @commands.is_owner()
    async def halt(self, ctx):
        """Halt the bot. Bot owner only."""
        if ctx.invoked_with == "kys":
            message = "Dead!"
        else:
            message = "Gonna halt now!"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """Restart the bot. Bot owner only."""
        message = "Restarting~"
        logger.warning(message)
        await ctx.send(message)
        await ctx.bot.logout()
        os.execl(sys.executable, sys.executable, *sys.argv)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Process())
