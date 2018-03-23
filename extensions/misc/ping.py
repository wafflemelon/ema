from datetime import datetime
import time
import discord

from discord.ext import commands


class Info:

    def __init__(self, bot):
        self.bot = bot
        self.initialtime = time.time()

    def getuptime(self):
        seconds = int(time.time() - self.initialtime)
        minutes = 0
        hours = 0
        days = 0

        if seconds > 86399:
            days = int(seconds / 86400)
            seconds = seconds % 86400
        if seconds > 3599:
            hours = int(seconds / 3600)
            seconds = seconds % 3600
        if seconds > 59:
            minutes = int(seconds / 60)
            seconds = seconds % 60

        return "{d}d {h}h {m}m {s}s".format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command()
    async def ping(self, ctx):
        """Get the latency and heartbeat"""
        pingpong = datetime.now() - ctx.message.created_at
        pingpong = pingpong.microseconds / 1000
        second = await ctx.send('hmmm?')
        heartbeat = second.created_at - ctx.message.created_at
        heartbeat = heartbeat.microseconds / 1000
        description = (
            '<:phong:421255541374058497> `' + str(pingpong) + ' ms`\n\n\n' +
            '<:hartz:421255540354711552> `' + str(heartbeat) + ' ms`'
        )

        embed = discord.Embed(description=description, color=0xB388FF)
        embed.set_thumbnail(
            url="https://p.apk4fun.com/66/19/e0/com.videogamepingpong-logo.jpg")
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await second.edit(new_content='*hmmm?*', embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """Uptime command"""
        await ctx.send(f"```{self.getuptime()}```")


def setup(bot):
    bot.add_cog(Info(bot))
