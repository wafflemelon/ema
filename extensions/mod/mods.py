import asyncio
import random
from collections import Counter

import discord
from discord.ext import commands


def are_overwrites_empty(self, overwrites):
    """There is currently no cleaner way to check if a
    PermissionOverwrite object is empty"""
    original = [p for p in iter(overwrites)]
    empty = [p for p in iter(discord.PermissionOverwrite())]
    return original == empty


def get_user(message, user):
    try:
        member = message.mentions[0]
    except:
        member = message.guild.get_member_named(user)
    if not member:
        try:
            member = message.guild.get_member(int(user))
        except ValueError:
            pass
    if not member:
        return None
    return member


def bool_converter(arg):
    arg = str(arg).lower()
    if arg in ["yes", "y", "true", "t", "1", "enable", "on"]:
        return True
    elif arg in ["no", "n", "false", "f", "0", "disable", "off"]:
        return False
    else:
        raise ValueError


class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['prune'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        """ Delete messages with a lot of options"""
    async def do_removal(self, message, limit, predicate):
        deleted = await message.channel.purge(limit=limit, before=message, check=predicate)
        spammers = Counter(m.author.display_name for m in deleted)
        messages = [f"<:garbage:421625880524226560> `{len(deleted)}` \nUsers:"]
        if len(deleted):
            messages.append('')
            spammers = sorted(spammers.items(),
                              key=lambda t: t[1], reverse=True)
            messages.extend(
                map(lambda t: '**{0[0]}**: {0[1]}'.format(t), spammers))

        await message.channel.send('\n'.join(messages), delete_after=5)

    @purge.command(pass_context=True)
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await self.do_removal(ctx.message, search, lambda e: len(e.embeds))

    @purge.command(pass_context=True)
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""
        await self.do_removal(ctx.message, search, lambda e: len(e.attachments))

    @purge.command(pass_context=True)
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""
        await self.do_removal(ctx.message, search, lambda e: len(e.embeds) or len(e.attachments))

    @purge.command(name='all', pass_context=True)
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""
        await self.do_removal(ctx.message, search, lambda e: True)

    @purge.command(pass_context=True)
    async def user(self, ctx, member: discord.Member, search=100):
        """Removes all messages by the member."""
        await self.do_removal(ctx.message, search, lambda e: e.author == member)

    @purge.command(pass_context=True)
    async def contains(self, ctx, *, substr: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """
        if len(substr) < 3:
            await ctx.send('The substring length must be at least 3 characters.')
            return

        await self.do_removal(ctx.message, 100, lambda e: substr in e.content)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member, *, reason:str=None):
        """Kicks a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.kick(reason=reason)
                await ctx.send(content=f'Kicked user: {user.mention}\nReason:**{reason}**')
            except discord.Forbidden:
                await ctx.send(content='Could not kick user. Not enough permissions.')
        else:
            return await ctx.send(content='Could not find user.')

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user: discord.Member, *, reason:str=None):
        """Bans a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                await ctx.send(content=f'Banned user: {user.mention}\nReason:**{reason}**')
            except discord.Forbidden:
                await ctx.send(content='Could not ban user. Not enough permissions.')
        else:
            return await ctx.send(content='Could not find user.')

    @commands.has_permissions(ban_members=True)
    @commands.command(aliases=['hban'])
    async def hackban(self, ctx, user_id: int, *, reason:str=None):
        """Bans a user outside of the server."""
        author = ctx.message.author
        guild = author.guild

        user = guild.get_member(user_id)
        if user is not None:
            await ctx.invoke(self.ban, user=user)
            return

        try:
            await self.bot.http.ban(user_id, guild.id, 0, reason=reason)
            await ctx.send(content=f'Banned user: {user_id}\nReason:**{reason}**')
        except discord.NotFound:
            await ctx.send(content='Could not find user. '
                           'Invalid user ID was provided.')
        except discord.errors.Forbidden:
            await ctx.send(content='Could not ban user. Not enough permissions.')

    @commands.has_permissions(ban_members=True)
    @commands.command(aliases=['sban'])
    async def softban(self, ctx, user: discord.Member, *, reason:str=None):
        """Softbans a user (if you have the permission)."""
        user = get_user(ctx.message, user)
        if user:
            try:
                await user.ban(reason=reason)
                await ctx.message.guild.unban(user, reason=reason)
                await ctx.send(content=f'Softbanned user: {user.mention}\nReason:**{reason}**')
            except discord.Forbidden:
                await ctx.send(content='Could not softban user. Not enough permissions.')
        else:
            return await ctx.send(content='Could not find user.')

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def banlist(self, ctx):
        """Displays the server's banlist"""
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Ban Members` permission")
            return
        bancount = len(banlist)
        display_bans = []
        bans = None
        if bancount == 0:
            bans = "No users are banned from this server"
        else:
            for ban in banlist:
                if len(", ".join(display_bans)) < 1800:
                    display_bans.append(str(ban.user))
                else:
                    bans = ", ".join(
                        display_bans) + "\n... and {} more".format(len(banlist) - len(display_bans))
                    break
        if not bans:
            bans = ", ".join(display_bans)
        await ctx.send("Total bans: `{}`\n```{}```".format(bancount, bans))

    @commands.command(description='Ping an online moderator.', aliases=['pingmod'])
    async def pingmods(self, ctx, *, reason: str = None):
        'Ping an online moderator.'

        mods = [i for i in ctx.guild.members if (i.permissions_in(ctx.channel).kick_members or i.permissions_in(ctx.channel).ban_members) and
                not i.bot and
                                                (i.status == discord.Status.online or i.status == ['online', 'idle', 'dnd'])]
        mod = random.choice(mods)
        reasonless_string = f'Mod Autoping: <@{mod.id}> (by **{ctx.author.name}**#{ctx.author.discriminator})'
        reason_string = f'Mod Autoping:\n**{reason}**\n<@{mod.id}> (by **{ctx.author.name}**#{ctx.author.discriminator})'
        await ctx.send(reason_string if reason != None else reasonless_string)

    @commands.command()
    async def guilds(self, ctx):
        """Returns a list of all Guilds that the Bot can see."""
        await ctx.send(embed=discord.Embed(
            title=f'Guilds ({sum(1 for _ in self.bot.guilds)} total)',
            description=', '.join(g.name for g in self.bot.guilds),
            colour=0x76FF03
        ))

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def addrole(self, ctx, user: discord.Member, *, name: str):
        """Adds the specified role to the specified user"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role with the name of `{}` was found on this server".format(name))
            return
        try:
            await user.add_roles(role, reason="The role \"{}\" was added by {}".format(role.name, ctx.author))
            await ctx.send("Successfully added the `{}` role to `{}`".format(name, user))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot add my highest role to users")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot add that role to users as it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def removerole(self, ctx, user: discord.Member, *, name: str):
        """Removes the specified role from the specified user"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role with the name of `{}` was found on this server".format(name))
            return
        try:
            await user.remove_roles(role, reason="The role \"{}\" was removed by {}".format(role.name, ctx.author))
            await ctx.send("Successfully removed the `{}` role from `{}`".format(name, user))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot remove my highest role from users")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot remove that role from users as it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def createrole(self, ctx, *, name: str):
        """Creates a role with the specified name"""
        try:
            await ctx.guild.create_role(name=name, reason="Created by {}".format(ctx.author), permissions=ctx.guild.default_role.permissions)
            await ctx.send("Successfully created a role named `{}`".format(name))
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Roles` permission")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def deleterole(self, ctx, *, name: str):
        """Deletes the role with the specified name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role was found on this server with the name of `{}`".format(name))
            return
        try:
            await role.delete(reason="Deleted by {}".format(ctx.author))
            await ctx.send("Successfully deleted the role named `{}`".format(name))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot delete my highest role")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot delete that role because it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def editrole(self, ctx, type: str, value: str, *, name: str):
        """Edits a role with the specified name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role was found on this server with the name of `{}`".format(name))
            return
        if type == "color":
            if value != "remove":
                try:
                    color = discord.Color(value=int(value.strip("#"), 16))
                except:
                    await ctx.send("`{}` is not a valid color. Make sure you are using a hex color! (Ex: #FF0000)".format(value))
                    return
            else:
                color = discord.Color.default()
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), color=color)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send("I cannot edit my highest role")
                elif role.position > ctx.me.top_role.position:
                    await ctx.send("I cannot edit that role because it is higher than my highest role")
                else:
                    await ctx.send("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                # Don't ask, for some reason if the role is higher than the bot's highest role it returns a NotFound 404 error
                await ctx.send("That role is higher than my highest role")
        elif type == "permissions":
            try:
                perms = discord.Permissions(permissions=int(value))
            except:
                await ctx.send("`{}` is not a valid permission number! If you need help finding the permission number, then go to <https://discordapi.com/permissions.html> for a permission calculator!".format(value))
                return
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), permissions=perms)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I either do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await ctx.send("That role is higher than my highest role")
        elif type == "position":
            try:
                pos = int(value)
            except:
                await self.bot.send_message(ctx.channel, "`" + value + "` is not a valid number")
                return
            if pos >= ctx.guild.me.top_role.position:
                await ctx.send("That number is not lower than my highest role's position. My highest role's permission is `{}`".format(ctx.guild.me.top_role.position))
                return
            try:
                if pos <= 0:
                    pos = 1
                await role.edit(reason="Moved by {}".format(ctx.author), position=pos)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await ctx.send("That role is higher than my highest role")
        elif type == "separate":
            try:
                bool = bool_converter(value)
            except ValueError:
                await ctx.send("`{}` is not a valid boolean".format(value))
                return
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), hoist=bool)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I do not have the `Manage Roles` permission or that role is not lower than my highest role.")
        elif type == "mentionable":
            try:
                bool = bool_converter(value)
            except ValueError:
                await ctx.send("`{}` is not a valid boolean".format(value))
                return
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), mentionable=bool)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await ctx.send("That role is higher than my highest role")
        else:
            await ctx.send("Invalid type specified, valid types are `color`, `permissions`, `position`, `separate`, and `mentionable`")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def renamerole(self, ctx, name: str, newname: str):
        """Renames a role with the specified name, be sure to put double quotes (\") around the name and the new name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role was found on this server with the name of `{}`".format(name))
            return
        try:
            await role.edit(reason="Renamed by {}".format(ctx.author), name=newname)
            await ctx.send("Successfully renamed the `{}` role to `{}`".format(name, newname))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot rename my highest role")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot rename that role because it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    # @commands.has_permissions(ban_members=True)
    # @commands.command()
    # async def massban(self, ctx, *, ids: str):
    #     """Mass bans users by ids (separate ids with spaces)"""
    #     await ctx.channel.trigger_typing()
    #     ids = ids.split(" ")
    #     failed_ids = []
    #     success = 0
    #     for id in ids:
    #         try:
    #             user = get_user(ctx.message, id)
    #             await user.ban
    #             success += 1
    #         except:
    #             failed_ids.append("`{}`".format(id))
    #     if len(failed_ids) != 0:
    #         await ctx.send("Failed to ban the following id(s): {}".format(", ".join(ids)))
    #     await ctx.send("Successfully banned {}/{} users".format(success, len(ids)))

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def removereactions(self, ctx, id: int):
        """Clear reactions from a message"""
        try:
            message = await ctx.channel.get_message(id)
        except discord.errors.NotFound:
            await ctx.send("I could not find a message with an ID of `{}` in this channel".format(id))
            return
        try:
            await message.clear_reactions()
            await ctx.send("Successfully cleared all the reactions from that message")
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Messages` permission")


def setup(bot):
    bot.add_cog(Moderation(bot))
