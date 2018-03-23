#!/usr/bin/env python3

"""Informational commands."""

import sys


import discord
from discord.ext import commands


class Info:
    """Commands that display information about the bot, user, etc."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Display guild (server) info.",
                      aliases=["guild", "ginfo", "server", "serverinfo", "sinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def guildinfo(self, ctx):
        """Display information about the current guild, such as owner, region, emojis, and roles."""

        guild = ctx.guild

        embed = discord.Embed(
            title=guild.name, color=0xB388FF)
        embed.description = guild.id

        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="Owner", value=str(guild.owner), inline=False)

        embed.add_field(name="Members", value=len(
            ctx.guild.members), inline=False)

        embed.add_field(name="Text channels", value=len(
            guild.text_channels), inline=False)
        embed.add_field(name="Voice channels", value=len(
            guild.voice_channels), inline=False)
        embed.add_field(name="Custom emojis", value=len(
            guild.emojis) or None, inline=False)
        embed.add_field(name="Custom roles",
                        value=len(guild.roles) - 1 or None, inline=False)
        embed.add_field(name="Roles",
                        value=', '.join(r.mention for r in guild.roles), inline=False)
        embed.add_field(name="Region", value=str(guild.region), inline=False)
        embed.add_field(name="Created at",
                        value=guild.created_at.ctime(), inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.command(brief="Display channel info.", aliases=["channel", "cinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def channelinfo(self, ctx, *, channel: discord.TextChannel=None):
        """Display information about a text channel."""

        # If channel is None, then it is set to ctx.channel.
        channel = channel or ctx.channel

        embed = discord.Embed(
            title=f"{channel.name}", color=0xB388FF)

        try:
            embed.description = channel.topic
        except AttributeError:
            pass

        embed.add_field(name="Channel ID", value=channel.id, inline=False)

        try:
            embed.add_field(
                name="Guild", value=channel.guild.name, inline=False)
        except AttributeError:
            pass

        embed.add_field(name="Members", value=len(
            channel.members), inline=False)
        embed.add_field(name="Created at",
                        value=channel.created_at.ctime(), inline=False)

        if channel.is_nsfw():
            embed.set_footer(text="NSFW content is allowed for this channel.")
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.command(brief="Display voice channel info.",
                      aliases=["voicechannel", "vchannel", "vcinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def vchannelinfo(self, ctx, *, channel: discord.VoiceChannel):
        """Display information about a voice channel."""

        embed = discord.Embed(
            title=f"{channel.name}", color=0xB388FF)
        embed.add_field(name="Channel ID", value=channel.id, inline=False)
        try:
            embed.add_field(
                name="Guild", value=channel.guild.name, inline=False)
        except AttributeError:
            pass
        embed.add_field(
            name="Bitrate", value=f"{channel.bitrate}bps", inline=False)
        if channel.user_limit > 0:
            user_limit = channel.user_limit
        else:
            user_limit = None
        embed.add_field(name="User limit", value=user_limit, inline=False)
        embed.add_field(name="Created at",
                        value=channel.created_at.ctime(), inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.command(brief="Display user info.", aliases=["user", "uinfo"])
    @commands.guild_only()
    @commands.cooldown(6, 12)
    async def userinfo(self, ctx, *, user: discord.Member=None):
        """Display information about a user, such as status and roles."""
        if not user:
            user = ctx.author

        embed = discord.Embed(title=f"{str(user)}")
        embed.colour = 0xB388FF

        embed.description = f"ID: {str(user.id)}"
        if user.activity:
            embed.description += f" | Playing **{user.activity.name}**"

        embed.set_thumbnail(url=user.avatar_url_as(format="png", size=128))

        embed.add_field(name="Nickname", value=user.nick, inline=False)
        embed.add_field(name="Bot user?",
                        value="Yes" if user.bot else "No", inline=False)

        # This is a bit awkward. Basically we don't want the bot to just say Dnd.
        if user.status.name == "dnd":
            status = "Do Not Disturb"
        else:
            status = user.status.name.capitalize()
        embed.add_field(name="Status", value=status, inline=False)

        embed.add_field(name="Joined guild at",
                        value=user.joined_at.ctime(), inline=False)
        embed.add_field(name="Joined Discord at",
                        value=user.created_at.ctime(), inline=False)

        # This is crap.
        roles = ", ".join(
            (role.mention for role in user.roles if not role.is_default()))[:1024]
        if roles:
            embed.add_field(name="Roles", value=roles, inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Info(bot))
