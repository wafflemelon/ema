import os

import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import textwrap


class Memes:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dipshit(self, ctx, msg: discord.Member=None):
        """Generate a meme
        usage : %prefix%dipshit <mention user>
        """
        if msg:
            msg = msg.name
        else:
            msg = ctx.author.name

        image = Image.open("data/google.jpg").convert("RGBA")
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

        font = ImageFont.truetype('data/fonts/arial.ttf', 18)

        d = ImageDraw.Draw(txt)

        d.text((138, 58), msg, font=font, fill=(0, 0, 0, 255))

        out = Image.alpha_composite(image, txt).save("dipshit.png")

        file = discord.File("dipshit.png", filename="dipshit.png")
        await ctx.trigger_typing()
        await ctx.send(file=file)
        os.remove('dipshit.png')

    @commands.command()
    async def headache(self, ctx, msg: discord.Member=None):
        """Generate a meme
        usage : %prefix%headache <mention user>
        """
        x = 396
        if msg:
            msg = msg.name
        else:
            msg = ctx.author.name

        if len(msg) > 8:
            x = x - 20

        image = Image.open("data/headache.png").convert("RGBA")
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

        font = ImageFont.truetype('data/fonts/impact.ttf', 54)

        d = ImageDraw.Draw(txt)

        d.text((361, 504), msg, font=font, fill=(0, 0, 0, 255))

        out = Image.alpha_composite(image, txt).save("headache.png")

        file = discord.File("headache.png", filename="headache.png")
        await ctx.trigger_typing()
        await ctx.send(file=file)
        os.remove('headache.png')

    @commands.command()
    async def firstwords(self, ctx, *, msg):
        """Generate a meme
        usage : %prefix%firstwords message
        """
        image = Image.open("data/firstwords.png").convert("RGBA")
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

        font = ImageFont.truetype('data/fonts/comic.ttf', 70)

        d = ImageDraw.Draw(txt)

        d.text((104, 27), f"{msg[0]}..{msg[0]}...",
               font=font, fill=(0, 0, 0, 255))

        out = Image.alpha_composite(image, txt)

        nfont = ImageFont.truetype('data/fonts/comic.ttf', 50)

        para = textwrap.wrap(msg, width=20)
        current_h = 591
        pad = 3
        for line in para:
            w, h = d.textsize(line, font=nfont)
            d.text((52, current_h), line, font=nfont, fill=(0, 0, 0, 255))
            current_h += h + pad

        img = Image.alpha_composite(out, txt).save("firstwords.png")

        file = discord.File("firstwords.png", filename="firstwords.png")
        await ctx.trigger_typing()
        await ctx.send(file=file)
        os.remove('firstwords.png')


def setup(bot):
    bot.add_cog(Memes(bot))
    