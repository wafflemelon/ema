"""A simple error handling extension. Should work with any discord.ext-based bot."""

from discord.ext import commands
from core.mysql import delete_data_entry


class IsNotHuman(commands.CommandError):
    """Raised if a bot attempts to invoke one of this bot's commands."""
    pass


def setup(bot):
    """Set up the cog."""

    @bot.check
    def is_human(ctx):
        """Prevent the bot from responding to other bots."""
        if ctx.author.bot:
            raise IsNotHuman("User is not human")
        return True

    @bot.listen("on_command_error")
    async def handle_error(ctx, exc):
        """Simple error handler."""
        if isinstance(exc, commands.MissingRequiredArgument):
            param = exc.param.replace("_", " ")
            await ctx.send(f"A {param} needs to be specified for this command to work.")
        elif not isinstance(exc, (commands.CommandNotFound, IsNotHuman)):
            await ctx.send(exc)

    @bot.listen("on_message")
    async def shhh(ctx):
        wlist = [110373943822540800, 264445053596991498]
        bot_num = len([a for a in ctx.guild.members if a.bot])
        percent = ((bot_num)/len(ctx.guild.members)) * 100
        if len(ctx.guild.members) > 40 and percent > 90 and ctx.guild.id not in wlist:
            return print("returned")
        else:
            pass
    

    @bot.listen("on_guild_remove")
    async def delguild(guild):
        wew = ["greet-message", "leave-message", "join-leave-channel", "join-role"]
        for owo in wew:
            delete_data_entry(guild.id, owo)
            print(f"Deleted {owo} in {guild.id}")


async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        return
    elif isinstance(error, commands.BadArgument):
        return


def is_owner():
    async def predicate(ctx):
        if str(ctx.author.id) in ctx.bot.config['owner']:
            return True
        else:
            False
    return commands.check(predicate)


def is_guild_owner():
    async def predicate(ctx):
        if ctx.author == ctx.guild.owner:
            return True
        else:
            False
    return commands.check(predicate)
