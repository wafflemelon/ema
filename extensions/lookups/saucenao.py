import asyncio
import re
from urllib.request import Request, urlopen

import discord
from bs4 import BeautifulSoup
from discord.ext import commands


async def get_image(channel, skip=0):
    """
    Searches the logs for a message with some sort of image attachment
    """
    async for message in channel.history(limit=100):
        for embed in message.embeds:
            if embed.thumbnail and embed.thumbnail.proxy_url:
                if skip <= 0:
                    return embed.thumbnail.proxy_url
                skip -= 1
        for attachment in message.attachments:
            if attachment.proxy_url:
                if skip <= 0:
                    return attachment.proxy_url
                skip -= 1


class Saucenao:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['source'])
    async def sauce(self, ctx, *, txt=None):
        """Find source of image using saucenao. 
        Example: %prefix%sauce https://images-na.ssl-images-amazon.com/images/I/71bSPK6-CJL._SL1500_.jpg"""
        if not txt:
            txt = await get_image(ctx.channel)

        elif txt is None and ctx.attachment:
            txt = ctx.attachment.proxy_url

        else:
            pass

        sauce_nao = 'http://saucenao.com/search.php?db=999&url='
        request_headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://thewebsite.com",
            "Connection": "keep-alive"
        }
        loop = asyncio.get_event_loop()
        try:
            req = Request(sauce_nao + txt, headers=request_headers)
            webpage = await loop.run_in_executor(None, urlopen, req)
        except:
            return await ctx.send('Exceeded daily request limit. Try again tomorrow, sorry!')
        soup = BeautifulSoup(webpage, 'html.parser')
        pretty_soup = soup.prettify()
        em = discord.Embed(color=0xB388FF)
        try:
            em.set_thumbnail(url=txt)
        except:
            pass
        match = re.findall(r'(?s)linkify" href="(.*?)"',
                           str(soup.find('div', id='middle')))
        title = re.findall(r'(?s)<div class="resulttitle">(.*?)</td',
                           str(soup.find('div', id='middle')))
        similarity_percent = re.findall(r'(?s)<div class="resultsimilarityinfo">(.*?)<',
                                        str(soup.find('div', id='middle')))
        ti = ''
        if title and float(similarity_percent[0][:-1]) > 60.0:
            title = title[0].strip().replace('<br/>', '\n').replace('<strong>', '').replace('</strong>', '').replace(
                '<div class="resultcontentcolumn">', '').replace('<span class="subtext">', '\n').replace('<small>',
                                                                                                         '').replace(
                '</span>', ' ').replace('</small>', '').replace('</tr>', '').replace('</td>', '').replace('</table>',
                                                                                                          '').replace(
                '</div>', '').split('\n')
            ti = '\n'.join([i.strip() for i in title if i.strip() != ''])
            if '</a>' not in ti:
                em.add_field(name='Source', value=ti)

            try:
                pretty_soup = pretty_soup.split(
                    'id="result-hidden-notification"', 1)[0]
            except:
                pass
            episode = re.findall(
                r'(?s)<span class="subtext">\n EP(.*?)<div', pretty_soup)
            ep = ''
            if episode:
                episode = episode[0].strip().replace('<br/>', '').replace('<strong>', '**').replace('</strong>',
                                                                                                    '**').replace(
                    '<span class="subtext">', '').replace('</span>', '').replace('</tr>', '').replace('</td>',
                                                                                                      '').replace(
                    '</table>', '').replace('</div>', '').split('\n')

                ep = ' '.join([j.strip() for j in episode if j.strip() != ''])
                ep = ep.replace('Est Time:', '\nEst Time:')
                em.add_field(name='More Info',
                             value='**Episode** ' + ep, inline=False)
            est_time = re.findall(r'(?s)Est Time:(.*?)<div', pretty_soup)
            if est_time and 'Est Time:' not in ep:
                est_time = est_time[0].strip().replace('<br/>', '').replace('<strong>', '').replace('</strong>',
                                                                                                    '').replace(
                    '<span class="subtext">', '').replace('</span>', '').replace('</tr>', '').replace('</td>',
                                                                                                      '').replace(
                    '</table>', '').replace('</div>', '').split('\n')

                est = ' '.join([j.strip()
                                for j in est_time if j.strip() != ''])
                est = est.replace('Est Time:', '\nEst Time:')
                em.add_field(name='More Info',
                             value='**Est Time:** ' + est, inline=False)

        sources = ''
        count = 0
        source_sites = {'www.pixiv.net': 'pixiv', 'danbooru': 'danbooru', 'seiga.nicovideo': 'nico nico seiga',
                        'yande.re': 'yande.re', 'openings.moe': 'openings.moe', 'fakku.net': 'fakku',
                        'gelbooru': 'gelbooru',
                        'deviantart': 'deviantart', 'bcy.net': 'bcy.net', 'konachan.com': 'konachan',
                        'anime-pictures.net': 'anime-pictures.net', 'drawr.net': 'drawr'}
        for i in match:
            if not i.startswith('http://saucenao.com'):
                if float(similarity_percent[count][:-1]) > 60.0:
                    link_to_site = '{} - {}, '.format(i,
                                                      similarity_percent[count])
                    for site in source_sites:
                        if site in i:
                            link_to_site = '[{}]({}) - {}, '.format(source_sites[site],
                                                                    i, similarity_percent[count])
                            break
                    sources += link_to_site
                    count += 1

            if count == 4:
                break
        sources = sources.rstrip(', ')

        material = re.search(r'(?s)Material:(.*?)</div',
                             str(soup.find('div', id='middle')))
        if material and ('Materials:' not in ti and 'Material:' not in ti):
            material_list = material.group(1).strip().replace('<br/>', '\n').replace('<strong>', '').replace(
                '</strong>', '').split('\n')
            mat = ', '.join([i.strip()
                             for i in material_list if i.strip() != ''])
            em.add_field(name='Material(s)', value=mat)

        characters = re.search(r'(?s)Characters:(.*?)</div',
                               str(soup.find('div', id='middle')))
        if characters and ('Characters:' not in ti and 'Character:' not in ti):
            characters_list = characters.group(1).strip().replace('<br/>', '\n').replace('<strong>', '').replace(
                '</strong>', '').split('\n')
            chars = ', '.join([i.strip()
                               for i in characters_list if i.strip() != ''])
            em.add_field(name='Character(s)', value=chars)

        creator = re.search(r'(?s)Creator:(.*?)</div',
                            str(soup.find('div', id='middle')))
        if creator and ('Creators:' not in ti and 'Creator:' not in ti):
            creator_list = creator.group(1).strip().replace('<br/>', '\n').replace('<strong>', '').replace('</strong>',
                                                                                                           '').split(
                '\n')
            creat = ', '.join([i.strip()
                               for i in creator_list if i.strip() != ''])
            em.add_field(name='Creator(s)', value=creat)

        if sources != '' and sources:
            em.add_field(name='Source sites - percent similarity',
                         value=sources, inline=False)

        if not sources and not creator and not characters and not material and not title or float(
                similarity_percent[0][:-1]) < 60.0:
            em = discord.Embed(
                color=0xB388FF, description="**Input:**\n{}\n\n**I didn't find anything :<**".format(txt))

        await ctx.send(content=None, embed=em)


def setup(bot):
    bot.add_cog(Saucenao(bot))
