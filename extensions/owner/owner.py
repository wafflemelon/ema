import discord
from discord.ext import commands
import urllib

from extensions.owner import handlers


class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def owner(self, ctx, action, user: discord.Member=None):
        """Add an Owner
        required args are {action} which includes `add`, `remove`, `list`
        {user} only required for `add` and `remove`.
        """
        owners = self.bot.config["owner"]
        if user is None:
            pass
        else:
            userid = str(user.id)

        if action == "add" and userid not in owners:
            owners.append(userid)
            await ctx.send("success!")
        elif action == "remove" and userid in owners:
            owners.remove(userid)
            await ctx.send("success!")
        elif action == "list" and user is None:
            ownerid = "\n".join(f"<@{i}>" for i in owners)
            embed = discord.Embed(color=0xB388FF)
            embed.title = "Owners"
            embed.description = (f"{ownerid}\n")
            await ctx.send(embed=embed)

        else:
            return await ctx.send("Woops! you did something wrong")

    @commands.command()
    @handlers.is_owner()
    async def rename(self, ctx, *, username):
        """Change the bot's username. Bot owner only.
        """
        await ctx.bot.user.edit(username=username)
        await ctx.send(f"Username changed x3")

    @commands.command()
    @handlers.is_owner()
    async def nick(self, ctx, *, nickname):
        """Change the bot's nickname. Bot owner only.
        """
        await ctx.me.edit(nick=nickname)
        await ctx.send(f"Nickname changed x3")

    @commands.command()
    @handlers.is_owner()
    async def setavatar(self, ctx, *, link: str):
        """Change the bot's avatar. Bot owner only.
        """
        try:
            with urllib.request.urlopen(link) as response:
                img = response.read()
                await ctx.bot.user.edit(avatar=img)
                await ctx.send("Avatar changed! ~~hopefully~~")
        except Exception as e:
            await ctx.send(f"Failed\n{e}")

    @commands.command(aliases=["sg", "game", "changegame"])
    @handlers.is_owner()
    async def setgame(self, ctx, *, game_name=None):
        """Change the bot's playing status. Bot owner only.
        """
        if game_name:
            name = f"{game_name} | [{(ctx.bot.shard_count)}]"
            game = discord.Game(name=name)
            await ctx.bot.change_presence(activity=game)
        elif game_name is None:
            name = f"{ctx.prefix}help | {ctx.bot.config['version']} | [{(ctx.bot.shard_count)}]"
            game = discord.Game(name=name)
            await ctx.bot.change_presence(activity=game)
        await ctx.send("Done~")

    @commands.command(aliases=["botpurge"])
    async def cleanup(self, ctx):
        """Delete the bot's previous message(s). Bot owner only.
        """
        times = 100
        times_executed = 0
        async for message in ctx.channel.history():
            if times_executed == times:
                break
            if message.author.id == ctx.bot.user.id:
                await message.delete()
                times_executed += 1
                
        await ctx.send(f"<:garbage:421625880524226560> `{times_executed}`", delete_after=5)

    @commands.command()
    async def test(self, ctx):
        """Delete the bot's previous message(s). Bot owner only.
        """
        
        await ctx.send("it worked you meme")



def setup(bot):
    bot.add_cog(Owner(bot))
