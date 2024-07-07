import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "ping")
    async def ping(self, ctx: commands.context):
        await ctx.send(f"Pong {round(self.bot.latency * 1000)}ms!")

    @commands.command(name = "kick")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx: commands.context, member: discord.Member, *, reason = None):
        kicker = ctx.author
        kicker_id = ctx.author.id

        if member.id == self.bot.user.id:
            await ctx.send("I can't kick myself!")
            return

        if reason is None:
            reason = "No reason provided."
        embed = discord.Embed(title = "Kicked", description = f"{member} has been kicked by {kicker} for {reason}",
                              color = discord.Color.red())

        # await member.kick(reason = reason)
        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Owner(bot))
