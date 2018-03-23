import datetime  # could have done wild card import but throws shit tons of warnings
from datetime import date
import discord
import faker
from discord.ext import commands


class Cnh:

    @commands.command(aliases=['cnh', 'CNH'])
    async def calvinandhobbes(self, ctx, year: int=None, month: int=None, day: int=None):
        """Module for Calvin and Hobbes Comics
        usage:
        %prefix%cnh (to get random comic)
        %prefix%cnh [year] [month] [day] (for specific day)
        """
        if year is None:
            fake = faker.Faker()
            # Calvin and Hobbes started on Nov 18, 1985 and ended Dec 31, 1995
            random = fake.date_between_dates(
                date_start=datetime.date(1985, 11, 18), date_end=datetime.date(1995, 12, 31))

            year = int(random.year)
            day = int(random.day)
            month = int(random.month)
        elif year and month and day:
            randomnum = f"{year}{month:02}{day:02}"
            if int(randomnum) > 19951231 or int(randomnum) < 19851118:
                await ctx.send("please enter valid date between 1985-11-18 and 1995-12-31!!")
                return
            else:
                pass

        else:
            return await ctx.send("please enter valid date between 1985-11-18 and 1995-12-31!!")

        link = f"http://marcel-oehler.marcellosendos.ch/comics/ch/{year}/{month:02}/{year}{month:02}{day:02}.gif"
        embed = discord.Embed(title="Calvin and Hobbes Comics", color=0xB388FF,
                              description=f"Date: {year}-{month:02}-{day:02}")

        embed.set_image(url=link)
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)


def setup(bot):
    """Calvin and Hobbles comics."""
    bot.add_cog(Cnh())
