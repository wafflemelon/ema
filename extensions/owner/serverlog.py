import discord


class serverlog:

    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        total = str(len(self.bot.guilds))
        embed = discord.Embed(color=0x76FF03)
        embed.description = f"I just joined __**{guild.name}**__ so the total number of guilds is: __**{total}**__"
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.add_field(name="ID", value=str(guild.id))
        embed.add_field(name="Members", value=len(guild.members))
        embed.add_field(name="Humans", value=len(guild.members) -
                        len([a for a in guild.members if a.bot]))
        bot_num = len([a for a in guild.members if a.bot])
        embed.add_field(name="Bots", value=str(bot_num))
        embed.add_field(name="Bot Percentage", value=str(
            ((bot_num)/len(guild.members)) * 100) + "%")
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Region", value=str(guild.region))
        channel = guild.text_channels[0]
        try:
            invite = await channel.create_invite()
            embed.add_field(name="Invite", value=invite)
        except Exception:
            pass

        await self.bot.get_guild(420889941602598913).get_channel(420905875700711425).send(embed=embed)

    async def on_guild_remove(self, guild):
        total = str(len(self.bot.guilds))
        embed = discord.Embed(color=0xFF1744)
        embed.description = f"I just left __**{guild.name}**__ so the total number of guilds is: __**{total}**__"
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.add_field(name="ID", value=str(guild.id))
        embed.add_field(name="Members", value=len(guild.members))
        embed.add_field(name="Humans", value=len(guild.members) -
                        len([a for a in guild.members if a.bot]))
        bot_num = len([a for a in guild.members if a.bot])
        embed.add_field(name="Bots", value=str(bot_num))
        embed.add_field(name="Bot Percentage", value=str(
            ((bot_num)/len(guild.members)) * 100) + "%")

        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Region", value=str(guild.region))
        # channel = guild.text_channels[0]
        # invite = await channel.create_invite()
        # embed.add_field(name="Invite", value=invite)

        await self.bot.get_guild(420889941602598913).get_channel(420905875700711425).send(embed=embed)


def setup(bot):
    bot.add_cog(serverlog(bot))


