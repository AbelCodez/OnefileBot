import discord
import time
from discord.ext import commands
from typing import Optional
from discord import Member
import random
import aiohttp
import json
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command
import datetime


TOKEN = (
    "YOUR_TOKEN"
    )

prefix = "+"
client = commands.Bot(command_prefix = prefix, intents=discord.Intents.all(), help_command=None)

Color = discord.Color.from_rgb(45, 123, 175)

@client.event
async def on_ready():
    print("Bot is ready!!!")

@client.command()
async def ping(ctx):
    embed = discord.Embed(color=Color)
    embed.add_field(
        name="Latency",
        value=f"{round(client.latency * 1000)}ms"
        )
    await ctx.send(embed=embed)

@client.command()
async def serverinfo(ctx):
    icon = ctx.guild.icon_url
    created = ctx.guild.created_at.strftime("%d/%m/%Y")
    embed = discord.Embed(title=f"{ctx.guild}\'s Information", color=Color)
    embed.set_thumbnail(
        url=icon
        )
    embed.add_field(
        name="Members",
        value=f"{ctx.guild.member_count}"
         )
    embed.add_field(
        name="Region",
        value=f"{ctx.guild.region}"
        )
    embed.add_field(
        name="Boosts",
        value=f"{ctx.guild.premium_subscription_count}"
        )
    embed.add_field(
        name="Roles",
        value=f"{len(ctx.guild.roles)}"
        )
    embed.add_field(
        name="Owner",
        value=f"{ctx.guild.owner}"
        )
    embed.add_field(
        name="Invites",
        value=f"{len(await ctx.guild.invites())}"
        )
    embed.set_footer(
        text=(f"Created at - {created}")
        )
    await ctx.send(embed=embed)

@client.command()
async def avatar(ctx, member: Optional[Member]):
    member = member or ctx.author
    avatar = member.avatar_url
    embed = discord.Embed(color=Color)
    embed.set_image(
        url=avatar
        )
    await ctx.send(embed=embed)

@client.command()
async def coinflip(ctx):
    embed = discord.Embed(color=Color, title="Flipping :coin:")
    msg = await ctx.channel.send(embed=embed)
    time.sleep(1)
    choices = ["Heads!", "Tails!"]
    embed=discord.Embed(color = Color, title=random.choice(choices))
    await msg.edit(embed=embed)

@client.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://aws.random.cat/meow') as r:
            res = await r.json()
            embed = discord.Embed(
                color=Color,
                title=f"Here's your cat {ctx.author}."
                )
            embed.set_image(url=res['file'])
            await ctx.send(embed=embed)

@client.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://random.dog/woof.json') as r:
            res = await r.json()
            embed = discord.Embed(
                color=Color,
                title=f"Here's your dog {ctx.author}."
                )
            embed.set_image(
                url=res['url']
                )
            await ctx.send(embed=embed)

@client.command()
async def userinfo(ctx, member: Optional[Member]):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"{member}'s' information",
        colour=Color
        )
    embed.set_thumbnail(
        url=member.avatar_url
        )
    embed.set_footer(
        text=f"ID {member.id}"
        )
    embed.add_field(
        name="Top role",
        value=member.top_role.mention
        )
    embed.add_field(
        name="Created at",
        value=member.created_at.strftime("%m/%d/%Y")
        )
    embed.add_field(
        name="Joined at",
        value=member.joined_at.strftime("%m/%d/%Y")
        )
    embed.add_field(
        name="Activity",
        value=f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}"
        )
    await ctx.send(embed=embed)

@client.command()
async def tinyurl(ctx, *, link: str):
    url = 'http://tinyurl.com/api-create.php?url=' + link
    async with aiohttp.ClientSession() as cs:
       async with cs.get(url) as r:
           new = await r.text()
           embed = discord.Embed(color=Color)
           embed.add_field(
               name="Original Link",
               value=link, inline=False
               )
           embed.add_field(
               name="Shortened Link",
               value=new, inline=False
               )
           await ctx.send(embed=embed)

@client.command()
async def help(ctx):
    embed = discord.Embed(colour=Color)
    embed.set_author(icon_url=client.user.avatar_url, name="Main Help:")
    embed.set_thumbnail(
        url=client.user.avatar_url
        )
    embed.add_field(
        name="ping",
        value="`Check bots ping`",
        inline=False
        )
    embed.add_field(
        name="serverinfo",
        value="`Get information about this server`",
        inline=False
        )
    embed.add_field(
        name="avatar",
        value="`Get a members avatar`",
        inline=False
        )
    embed.add_field(
        name="coinflip",
        value="`Flip a coin`",
        inline=False
        )
    embed.add_field(
        name="dog",
        value="`Picture of a doggo`",
        inline=False
    )
    embed.add_field(
        name="cat",
        value="`Picture of a cat`",
        inline=False
        )
    embed.add_field(
        name="userinfo",
        value="`Information about a user`",
        inline=False
        )
    embed.add_field(
        name="tinyurl",
        value="`Shorten a link`",
        inline=False
        )
    embed.add_field(
        name="poll",
        value="`Create a poll`",
        inline=False
        )
    embed.add_field(
        name="threats",
        value="`Biggest threats to society`"
        )
    await ctx.send(embed=embed)

@client.command()
async def poll(context, *args):
    poll_title = " ".join(args)
    embed = discord.Embed(
        title=f"{poll_title}",
        color=Color
    )
    embed.set_footer(
        text=f"Poll created by: {context.message.author} • React to vote!"
    )
    embed_message = await context.send(embed=embed)
    await embed_message.add_reaction("👍")
    await embed_message.add_reaction("👎")
    await embed_message.add_reaction("🤷")

@client.command()
async def threats(ctx, target: Optional[Member]):
    target = target or ctx.author
    picture = target.avatar_url_as(size=1024, format=None, static_format='png')
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={picture}") as r:
            res = await r.json()
            embed = discord.Embed(
                color=Color
            )
            embed.set_image(
                url=res["message"]
                )

            await ctx.send(embed=embed)


client.run(TOKEN)
