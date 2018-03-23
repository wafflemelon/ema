from discord.ext import commands
import discord
from extensions.owner import handlers

from core.mysql import *


class Settings:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set")
    @commands.has_permissions(manage_guild=True)
    async def _set(self, ctx, thing, *, value: str=None):
        """Here you can set join messages, leave messages, join role and join/leave message channel.
        * thing: it can be `greet-message`, `leave-message`, `join-role`, `join-leave-channel`
        * value: for the greet / leave messages the value will be the message
        example: Hello there! %user%. Welcome to %guild%
        here `%user%` and `%guild%` are the new user mention and name of the guild respectively.
        for join role, just type in the exact role name (role names are case sensitive)
        same goes for join-leave-channel.
        """

        if thing == "greet-message":
            if value == "remove":
                update_data_entry(ctx.guild.id, "greet-message", None)
                await ctx.send(f"Removed {thing}")
            else:
                update_data_entry(ctx.guild.id, "greet-message", value)
                join_message = value.replace(
                    "%user%", ctx.author.mention).replace("%guild%", ctx.guild.name)
                await ctx.send(f"Your new greeting message is:\n**{join_message}**")
        elif thing == "leave-message":
            if value == "remove":
                update_data_entry(ctx.guild.id, "leave-message", None)
                await ctx.send(f"Removed {thing}")
            else:
                update_data_entry(ctx.guild.id, "leave-message", value)
                leave_message = value.replace(
                    "%user%", ctx.author.mention).replace("%guild%", ctx.guild.name)
                await ctx.send(f"Your new goodbye message is:\n**{leave_message}**")
        elif thing == "join-leave-channel":
            if value == "remove":
                update_data_entry(ctx.guild.id, "join-leave-channel", None)
                await ctx.send(f"Removed {thing}")
            elif value is None:
                update_data_entry(ctx.guild.id,
                                  "join-leave-channel", ctx.channel.name)
                await ctx.send(f"The channel {ctx.channel.mention}, has been set as greet/goodbye channel")
            else:
                channel = discord.utils.get(ctx.guild.channels, name=value)
                if channel:
                    update_data_entry(ctx.guild.id,
                                      "join-leave-channel", channel.name)
                    await ctx.send(f"The channel {channel.mention}, has been set as greet/goodbye channel")
                else:
                    return await ctx.send("Invalid channel")

        elif thing == "join-role":
            if value == "remove":
                update_data_entry(ctx.guild.id, "join-role", None)
                await ctx.send(f"Removed {thing}")
            else:
                role = discord.utils.get(ctx.guild.roles, name=value)
                update_data_entry(ctx.guild.id, "join-role", role.name)
                await ctx.send(f"The new join role is {role.mention}")

        # elif thing == "mod-log-channel": HAHAHA MODLOGS LATER
        #
        #     if value == "remove":
        #         update_data_entry(ctx.guild.id, "mod-log-channel", None)
        #         await ctx.send(f"Removed {thing}")
        #     elif value is None:
        #         update_data_entry(ctx.guild.id,
        #                           "mod-log-channel", ctx.channel.name)
        #         await ctx.send(f"The channel {ctx.channel.mention}, has been set as mod log channel")
        #     else:
        #         channel = discord.utils.get(ctx.guild.channels, name=value)
        #         update_data_entry(ctx.guild.id,
        #                           "mod-log-channel", channel.name)
        #         await ctx.send(f"The channel {channel.mention}, has been set as mod log channel")

        else:
            await ctx.send("Please use the command with proper arguments")

    @commands.command()
    async def configs(self, ctx):
        """Shows the on user join and leave configuration"""
        embed = discord.Embed(color=0xB388FF)
        embed.title = "SERVER CONFIGURATION"
        greet_message = read_data_entry(ctx.guild.id, "greet-message")
        if greet_message:
            pass
        else:
            greet_message = "None"
        leave_message = read_data_entry(ctx.guild.id, "leave-message")
        if leave_message:
            pass
        else:
            leave_message = "None"

        join_role = read_data_entry(ctx.guild.id, "join-role")
        if join_role:
            role = discord.utils.get(ctx.guild.roles, name=join_role)
            join_role = role.mention
            pass
        else:
            join_role = "None"

        join_leave_channel = read_data_entry(
            ctx.guild.id, "join-leave-channel")

        if join_leave_channel:
            channel = discord.utils.get(
                ctx.guild.channels, name=join_leave_channel)
            join_leave_channel = channel.mention
        else:
            join_leave_channel = "None"

        mod_channel = read_data_entry(ctx.guild.id, "mod-log-channel")
        if mod_channel:
            channel = discord.utils.get(ctx.guild.channels, name=mod_channel)
            mod_channel = channel.mention
        else:
            mod_channel = "None"

        embed.add_field(name="Join message", value=greet_message, inline=False)
        embed.add_field(name="Leave message", value=leave_message)
        embed.add_field(name="Join/leave",
                        value=join_leave_channel, inline=False)
        embed.add_field(name="Join Role", value=join_role)
        # embed.add_field(name="Mod log channel",
        #                 value=mod_channel, inline=False)
        print(greet_message, leave_message, join_leave_channel, join_role)
        await ctx.send(embed=embed)


def setup(bot):
    """Set up the extension."""
    bot.add_cog(Settings(bot))
