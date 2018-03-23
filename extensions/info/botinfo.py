import os
import sys
import time

import discord
import psutil
from discord.ext import commands

from extensions.misc import ping

try:
    import core
except ImportError:
    core = False


class BotInfo:
    def __init__(self, bot):
        self.bot = bot
        self.initialtime = time.time()

    def humanbytes(self, B):  # function lifted from StackOverflow :mmLol:
        'Return the given bytes as a human friendly KB, MB, GB, or TB string'
        B = float(B)
        KB = float(1024)
        MB = float(KB ** 2)  # 1,048,576
        GB = float(KB ** 3)  # 1,073,741,824
        TB = float(KB ** 4)  # 1,099,511,627,776

        if B < KB:
            return '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
        elif KB <= B < MB:
            return '{0:.2f} KB'.format(B/KB)
        elif MB <= B < GB:
            return '{0:.2f} MB'.format(B/MB)
        elif GB <= B < TB:
            return '{0:.2f} GB'.format(B/GB)
        elif TB <= B:
            return '{0:.2f} TB'.format(B/TB)

    @commands.command(aliases=["stats", "botstats", "info"])
    async def botinfo(self, ctx):
        """Information regarding the bot"""
        mem = psutil.virtual_memory()
        currproc = psutil.Process(os.getpid())
        total_ram = self.humanbytes(mem[0])
        available_ram = self.humanbytes(mem[1])
        usage = self.humanbytes(currproc.memory_info().rss)
        embed = discord.Embed()
        embed.title = "Ema Yasuhara"
        if core:
            embed.description = core.description
        else:
            pass
        embed.colour = 0xB388FF
        appinfo = await ctx.bot.application_info()
        owner = str(appinfo.owner)
        embed.add_field(name="Owner", value=owner)
        embed.add_field(name="# of commands", value=len(ctx.bot.commands))
        if ctx.guild and ctx.bot.shard_count > 1:
            embed.add_field(
                name="Shard", value=f"{ctx.guild.shard_id+1} of {ctx.bot.shard_count}")

        embed.add_field(name="Servers", value=len(ctx.bot.guilds))
        num_users = len(
            list(filter(lambda member: not member.bot, ctx.bot.get_all_members())))
        embed.add_field(name="Total Members", value=num_users)
        embed.add_field(name="Version", value=self.bot.config["version"])
        embed.add_field(
            name="Python", value="{0}.{1}.{2}".format(*sys.version_info))
        embed.add_field(name="discord.py", value=discord.__version__)
        embed.add_field(name="Uptime", value=ping.Info.getuptime(self))
        embed.add_field(name="Total RAM", value=f"{total_ram}")
        embed.add_field(name="Available RAM", value=f"{available_ram}")
        embed.add_field(name="RAM used by me", value=f"{usage}")
        embed.add_field(name="Github Repository:", value="https://github.com/wafflemelon/ema")
        embed.add_field(name="support server",
                        value="https://discord.gg/2YcPwgt")
        embed.set_thumbnail(url=ctx.bot.user.avatar_url_as(format="png"))
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.command()
    async def creds(self, ctx):
        embed = discord.Embed(color=0xB388FF)
        embed.title = "Credits"
        embed.description = "These people helped make Ema possible"
        embed.add_field(
            name="Ry00001", value="For the evalualtion and shell command")
        embed.add_field(name="Waffles (me)", value="HEHEHE", inline=False)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BotInfo(bot))
