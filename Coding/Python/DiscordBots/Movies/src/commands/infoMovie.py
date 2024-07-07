import discord
import discord.bot
from discord.ext import commands

import aiohttp
import json
import datetime

rates = {
  "G": "https://help.imdb.com/article/contribution/titles/certificates/GU757M8ZJ9ZPXB39?ref_=helpart_nav_27#:~:text=G%20%2D-,For%20all%20audiences,-PG%20%2D%20Parental%20Guidance",
  "PG": "https://help.imdb.com/article/contribution/titles/certificates/GU757M8ZJ9ZPXB39?ref_=helpart_nav_27#:~:text=Parental%20Guidance%20Suggested%20(mainly%20for%20under%2010%27s)",
  "PG-13": "https://help.imdb.com/article/contribution/titles/certificates/GU757M8ZJ9ZPXB39?ref_=helpart_nav_27#:~:text=PG%2D13%20%2D-,Parental%20Guidance%20Suggested%20for%20children%20under%2013,-R%20%2D%20Under%2017",
  "R": "https://help.imdb.com/article/contribution/titles/certificates/GU757M8ZJ9ZPXB39?ref_=helpart_nav_27#:~:text=Under%2017%20not%20admitted%20without%20parent%20or%20guardian",
  "NC-17": "https://help.imdb.com/article/contribution/titles/certificates/GU757M8ZJ9ZPXB39?ref_=helpart_nav_27#:~:text=NC%2D17%20%2D-,Under%2017%20not%20admitted,-Approved%20%2D%20Pre%2D1968",
  "N/A": "N/A"
}


class info_movie(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot: discord.Bot = bot

  moviesCommands = discord.SlashCommandGroup(
    "movie", "Everything the bots Offer About Movies"
  )

  @moviesCommands.command(name="info", description="Get Info About Any Movie")
  async def info_about_movie(self, ctx: discord.ApplicationContext, name) -> None:
    url = f"http://www.omdbapi.com/?t={name}&apikey=11634dc"

    async with aiohttp.ClientSession() as session:
      async with session.get(url) as resp:
        print(resp.status)
        
        info =json.loads(await resp.text())
        
        embed = discord.Embed(
          title=f"**{info["Title"]}**",
          description=f"{info["Plot"]}",
          colour=0xFFFFFF,
          timestamp=datetime.datetime.now(),
        )

        embed.set_author(name=f"{info["Director"]}")

        embed.add_field(
          name=":hash: Genre", value=f"{info["Genre"]}", inline=True
        )
        embed.add_field(
          name=":identification_card: Rating",
          value=f"[{info["Rated"]}]({rates[info["Rated"]]})",
          inline=True,
        )
        
        min = [int(i) for i in f"{info["Runtime"]}".split() if i.isdigit()][0]
        h=min//60
        m=min%60
        
        embed.add_field(
          name=":hourglass_flowing_sand: Duration",
          value=f"{info["Runtime"]} ({h}h {m}m)",
          inline=True,
        )
        embed.add_field(
          name=":inbox_tray: Imdb Rating",
          value=f":arrow_up_small: {info["imdbRating"]} ({info["imdbVotes"]} Votes)",
          inline=True,
        )
        embed.add_field(name=":map: Language", value=f"{info["Language"]}", inline=True)
        embed.add_field(
          name=":asterisk: Type", value=f":movie_camera: {info["Type"]}", inline=True
        )
        embed.add_field(
          name=":trophy: Awards",
          value=f"{info["Awards"]}",
          inline=False,
        )

        embed.set_image(
          url=f"{info["Poster"]}"
        )

        embed.set_footer(
          text=f"Released: {info["Released"]}", icon_url="https://slate.dan.onl/slate.png"
        )

        await ctx.send_response(embed=embed)

    pass


def setup(bot: discord.Bot):
    bot.add_cog(info_movie(bot))


