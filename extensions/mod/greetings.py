from core.mysql import *


def setup(bot):
    """Sets up the extension."""

    @bot.listen("on_guild.leave")
    async def delete_entries(guild):
        varrs = ["greet-message", "join-role", "join-leave-channel",
                 "leave-message", "mod-log-channel"]
        for entries in varrs:
            delete_data_entry(guild.id, entries)

    @bot.listen("on_member_join")
    async def joinmsg(member: discord.Member):
        join_message = read_data_entry(member.guild.id, "greet-message")
        if join_message:
            join_message = join_message.replace(
                "%user%", member.mention).replace("%guild%", member.guild.name)
        join_leave_channel_name = read_data_entry(
            member.guild.id, "join-leave-channel")

        join_leave_channel_name = read_data_entry(
            member.guild.id, "join-leave-channel")
        if join_leave_channel_name:
            join_leave_channel = discord.utils.get(
                member.guild.channels, name=join_leave_channel_name)
        else:
            join_leave_channel = None
        join_role_name = read_data_entry(member.guild.id, "join-role")
        if join_role_name:
            join_role = discord.utils.get(
                member.guild.roles, name=join_role_name)
            if join_role is None:
                update_data_entry(member.guild.id, "join-role", None)
        else:
            join_role = None
        if join_leave_channel and join_message:
            try:
                await join_leave_channel.send(join_message)
            except:
                pass
        if join_role:
            try:
                await member.add_roles(join_role)
            except:
                None

    @bot.listen("on_member_remove")
    async def byemsg(member: discord.Member):
        leave_message = read_data_entry(member.guild.id, "leave-message")
        if leave_message:
            leave_message = leave_message.replace(
                "%user%", member.mention).replace("%guild%", member.guild.name)
        join_leave_channel_name = read_data_entry(
            member.guild.id, "join-leave-channel")
        if join_leave_channel_name:
            join_leave_channel = discord.utils.get(
                member.guild.channels, name=join_leave_channel_name)
        else:
            join_leave_channel = None

        if join_leave_channel and leave_message:
            try:
                await join_leave_channel.send(leave_message)
            except:
                print("shit happened")
                pass
