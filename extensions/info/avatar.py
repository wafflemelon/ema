
import random
import discord
from discord.ext import commands


class Avatar:
    """Avatar commands."""

    @commands.command()
    @commands.cooldown(6, 12)
    async def avatar(self, ctx, *, user: discord.Member=None):
        """Display a user's avatar.
        Defaults to displaying the avatar of the user who invoked the command."""
        if not user:
            user = ctx.author
        embed = discord.Embed(color=0xB388FF)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.command(aliases=["gicon", "servericon", "sicon"])
    @commands.cooldown(6, 12)
    async def guildicon(self, ctx):
        """Display the icon of the current guild."""
        embed = discord.Embed(color=0xB388FF)
        embed.set_image(url=ctx.guild.icon_url)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Avatar())
