#!/usr/bin/env python3

"""Command logging functionality."""

import logging

FORMAT = "%(asctime)-15s: %(message)s"
formatter = logging.Formatter(FORMAT)

def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_command")
    async def log_command(ctx):
        message = (f"{ctx.message.content} | "
                   f"{ctx.author.name}:{ctx.author.id} in {ctx.guild.name}:{ctx.guild.id}")
        message = f"{ctx.message.created_at.ctime()}: {message}"

        print(message)

       #RIP command logging line 