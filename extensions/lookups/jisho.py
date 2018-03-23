#!/usr/bin/env python3

"""jisho.org query command."""

import urllib.parse
import requests

import discord
from discord.ext import commands

BASE_URL = "http://jisho.org/api/v1/search/words"


class Jisho:
    """A Japanese translation command."""

    @commands.command(aliases=["jp"])
    async def jisho(self, ctx, query):
        """Translate a word into Japanese.
        Example usage:
        %prefix%jisho kawaii
        """
        with requests.get(BASE_URL, params={"keyword": query}) as response:
            data = response.json()

            if not data["data"]:
                await ctx.send("No matching result found on jisho.org.")

            jap = data["data"][0]["japanese"][0]
            senses = data["data"][0]["senses"][0]
            defs = ", ".join(senses["english_definitions"])
            tags = senses["tags"]

            embed = discord.Embed(color=0xB388FF)
            embed.add_field(name="Kanji", value=str(jap.get("word")))
            embed.add_field(name="Kana", value=str(
                jap.get("reading")), inline=False)
            embed.add_field(name="English", value=defs, inline=False)
            embed.add_field(name="Tags", value=tags)
            embed.set_thumbnail(
                url="https://www.tofugu.com/images/learn-japanese/jisho-org-9a549ffd.jpg")
            embed.set_footer(
                text=f"Requested by {ctx.author.name} | Powered by jisho.org", icon_url=ctx.author.avatar_url_as(format="png"))
            await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Jisho())
