#!/usr/bin/env python3
import json
from urllib import parse

import discord
import requests
from discord.ext import commands


class Dictionary:
    """Urban Dictionary lookup command."""

    @commands.command(pass_context=True, aliases=['urban', "ud"])
    async def urbandictionary(self, ctx, *, msg):
        """Pull data from Urban Dictionary. Use ema help ud for more information.
        Usage: %prefix%ud <term> - Search for a term on Urban Dictionary.
        You can pick a specific result with %prefix%<term> | <result>.
        If no result is specified, the first result will be used.
        """
        number = 1
        if " | " in msg:
            msg, number = msg.rsplit(" | ", 1)
        search = parse.quote(msg)
        response = requests.get(
            "http://api.urbandictionary.com/v0/define?term={}".format(search)).text
        result = json.loads(response)
        if result["result_type"] == "no_results":
            await ctx.send("{} couldn't be found on Urban Dictionary.".format(msg))
        else:
            try:
                top_result = result["list"][int(number) - 1]
                embed = discord.Embed(title=top_result["word"], description=top_result["definition"],
                                      url=top_result["permalink"], color=0xB388FF)
                if top_result["example"]:
                    embed.add_field(name="Example:",
                                    value=top_result["example"])
                if result["tags"]:
                    embed.add_field(
                        name="Tags:", value=" ".join(result["tags"]))
                embed.set_author(name=top_result["author"],
                                 icon_url="https://apprecs.org/gp/images/app-icons/300/2f/info.tuohuang.urbandict.jpg")
                number = str(int(number) + 1)
                embed.set_footer(text=str(len(
                    result["list"])) + f" results were found. To see a different result, use ema ud {msg} | {number}.")
                await ctx.send("", embed=embed)
            except IndexError:
                await ctx.send(f"That result doesn't exist! Try ema ud {msg}.")


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Dictionary())
