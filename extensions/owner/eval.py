import subprocess
import textwrap
import time

import aiohttp
import discord
from discord.ext import commands

from extensions.owner import handlers


class Evaluation:
    def __init__(self, bot):
        self.bot = bot
        self._eval = {}

    async def haste_get(self, output):
        with aiohttp.ClientSession() as sess:
            async with sess.post("https://hastebin.com/documents/", data=output, headers={"Content-Type": "text/plain"}) as r:
                r = await r.json()
                return (f"https://hastebin.com/{r['key']}")

    @commands.command(aliases=["ev", "e"])
    @handlers.is_owner()
    async def eval(self, ctx, *, code: str):
        """Evaluates Python code"""
        if self._eval.get('env') is None:
            self._eval['env'] = {}
        if self._eval.get('count') is None:
            self._eval['count'] = 0

        codebyspace = code.split(" ")
        print(codebyspace)
        silent = False
        if codebyspace[0] == "--silent" or codebyspace[0] == "-s":
            silent = True
            print("silent mmLol")
            codebyspace = codebyspace[1:]
            code = " ".join(codebyspace)

        self._eval['env'].update({
            'self': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'channel': ctx.message.channel,
            'guild': ctx.message.guild,
            'author': ctx.message.author,
        })

        # let's make this safe to work with
        code = code.replace('```py\n', '').replace('```', '').replace('`', '')

        _code = 'async def func(self):\n  try:\n{}\n  finally:\n    self._eval[\'env\'].update(locals())'\
            .format(textwrap.indent(code, '    '))

        before = time.monotonic()
        # noinspection PyBroadException
        try:
            exec(_code, self._eval['env'])
            func = self._eval['env']['func']
            output = await func(self)

            if output is not None:
                output = repr(output)
        except Exception as e:
            output = '{}: {}'.format(type(e).__name__, e)
        after = time.monotonic()
        self._eval['count'] += 1
        count = self._eval['count']

        code = code.split('\n')
        if len(code) == 1:
            _in = 'In [{}]: {}'.format(count, code[0])
        else:
            _first_line = code[0]
            _rest = code[1:]
            _rest = '\n'.join(_rest)
            _countlen = len(str(count)) + 2
            _rest = textwrap.indent(_rest, '...: ')
            _rest = textwrap.indent(_rest, ' ' * _countlen)
            _in = 'In [{}]: {}\n{}'.format(count, _first_line, _rest)

        message = '```py\n{}'.format(_in)
        if output is not None:
            message += '\nOut[{}]: {}'.format(count, output)
        ms = int(round((after - before) * 1000))
        if ms > 100:  # noticeable delay
            message += '\n# {} ms\n```'.format(ms)
        else:
            message += '\n```'

        try:
            if ctx.author.id == self.bot.user.id:
                await ctx.message.edit(content=message)
            else:
                if not silent:
                    await ctx.send(message)
        except discord.HTTPException:
            url = await self.haste_get(output)
            embed = discord.Embed(
                description=f"[View output - click]({url})", color=0xB388FF)
            await ctx.send(embed=embed)

    @commands.command(aliases=['sys', 's', 'run'], description="Run system commands.")
    @handlers.is_owner()
    async def system(self, ctx, *, command: str):
        'Run system commands.'
        process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        result = process.communicate()
        embed = discord.Embed(
            title="Command output",
            color=0xB388FF
        )
        if result[0] is not None:
            stdout = result[0].decode('utf-8')
        if result[1] is not None:
            stderr = result[1].decode('utf-8')
        try:
            embed.add_field(name="stdout", value=f'```{stdout}```' if 'stdout' in locals(
            ) else 'No output.', inline=False)
            embed.add_field(name="stderr", value=f'```{stderr}```' if 'stderr' in locals(
            ) else 'No output.', inline=False)
            embed.set_footer(
                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url_as(format="png"))
            await ctx.send(embed=embed)
        except discord.HTTPException:
            with aiohttp.ClientSession() as sess:
                url = await self.haste_get(stdout)
                embed = discord.Embed(
                    description=f"[View output - click]({url})", color=0xB388FF)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Evaluation(bot))
