#!/usr/bin/env python3

"""Contains a cog with the bot's invite command."""

import discord
from discord.ext import commands


class Invite:
    """Invite command."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def invite(self, ctx):
        """Generate an invite link for this bot."""
        invite_minimal = ("[Minimal invite](https://discordapp.com/oauth2/authorize?"
                          f"client_id={ctx.bot.user.id}&scope=bot)")
        invite_full = ("[Invite with permissions](https://discordapp.com/oauth2/authorize?"
                       f"permissions=8&client_id={ctx.bot.user.id}&scope=bot)")
        support_server = "https://discord.gg/2YcPwgt"
        embed = discord.Embed(title="Help yourself with either of the following links!", color=0xB388FF)
        embed.description = "\n".join((invite_minimal, invite_full))
        embed.add_field(name='Support', value='[Link]({})'.format(support_server))
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Invite())
