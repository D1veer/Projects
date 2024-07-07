import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "information", aliases = ["info"], brief = "Information about the bot.")
    async def info(self, ctx: commands.context):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner.id)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        member_count = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        created_at_var = ctx.guild.created_at

        channles = ctx.guild.channels
        channels_count = 0
        for i in channles:
            channels_count += 1
        new_created_at = created_at_var.strftime("%m/%d/%Y, %H:%M:%S")
        channles_texts = ctx.guild.text_channels
        channles_voices = ctx.guild.voice_channels

        channels_texts_count = 0
        for v in channles_texts:
            channels_texts_count += 1
        channels_voices_count = 0
        for v in channles_voices:
            channels_voices_count += 1

        embad = discord.Embed(
            title = "",
            image = icon,
            description = "",
            icon = icon,
            colour = discord.Colour.blue()
        )
        embad.set_thumbnail(url = icon)
        embad.set_author(name = name + " Server Information.", icon_url = icon)
        embad.add_field(name = "Server ID :id:", value = id, inline = True)
        embad.add_field(name = "Created At :calendar:", value = new_created_at, inline = True)
        embad.add_field(name = "Owner :crown:", value = f"<@{owner}>", inline = True)
        embad.add_field(name = "Region :earth_asia:", value = region, inline = True)
        embad.add_field(name = f"Channels ({channels_count}) :speech_balloon:",
                        value = f"**{channels_texts_count}** Text | **{channels_voices_count}** Voice", inline = True)
        embad.add_field(name = "Member Count :busts_in_silhouette:", value = member_count, inline = True)
        embad.set_footer(text = "2021 SquareMC Official. All Rights Reserved.",
                         icon_url = "https://img.icons8.com/ios-glyphs/30/ffffff/copyright.png")

        await ctx.send(embed = embad)

    @commands.command(name = "help", aliases = ["h"], brief = "Help command.")
    async def help(self, ctx: commands.context):
        embad = discord.Embed(
            title = "",
            description = "",

            colour = discord.Colour.blue()
        )
        embad.set_author(name = "Help Command.", icon_url = "https://img.icons8.com/ios-glyphs/30/ffffff/copyright.png")
        embad.add_field(name = "**Information**", value = "**information** | **info**", inline = False)
        embad.add_field(name = "**Help**", value = "**help** | **h**", inline = False)
        embad.add_field(name = "**Ping**", value = "**ping**", inline = False)
        embad.add_field(name = "**Invite**", value = "**invite**", inline = False)
        embad.add_field(name = "**Bot**", value = "**bot**", inline = False)
        embad.add_field(name = "**Bot Info**", value = "**botinfo** | **botinformation**", inline = False)
        embad.add_field(name = "**Bot Owner**", value = "**botowner** | **botownerinfo**", inline = False)
        embad.add_field(name = "**Bot Support**", value = "**botsupport** | **botsupportinfo**", inline = False)
        embad.add_field(name = "**Bot Creator**", value = "**botcreator** | **botcreatorinfo**", inline = False)
        await ctx.send(embed = embad)



def setup(bot):
    bot.add_cog(Music(bot))
