from datetime import datetime
import requests
from sportsipy.fb.roster import SquadPlayer
from sportsipy.fb.team import Team, Roster
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
import pycountry

countries = {}
for country in pycountry.countries:
  countries[country.name] = country.alpha_2

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = "!", intents = intents)
client.remove_command("help")


@client.command("Team", alias=["team"])
async def get_team_data(ctx, *, TeamName):
  teamName = ""
  teamCountry = ""
  teamRecord = ""
  teamManager = ""
  teamGoals_scored = ""
  teamPoints = ""
  teamPosition = ""
  teamLeague = ""
  teamGender = ""
  teamExpected_goals = ""
  teamSquad_id = ""
  try:
    team = Team(TeamName)
    teamName = TeamName
    teamCountry = team.country
    teamRecord = team.record
    teamManager = team.manager
    teamGoals_scored = team.goals_scored
    teamPoints = team.points
    teamPosition = team.position
    teamLeague = team.league
    teamGender = team.gender
    teamExpected_goals = team.expected_goals
    teamSquad_id = team.squad_id
  except ValueError as ve:
    await ctx.send(f"⛔ Error: {ve}")

  URL = f"https://fbref.com/en/squads/{teamSquad_id}/"
  r = requests.get(URL)
  soup = BeautifulSoup(r.content, 'html.parser')
  myimg = soup.find_all("img", {"class": "teamlogo"})
  logo_url = ""
  if len(myimg) > 0:
    logo_url = myimg[0]["src"]
  country_code = countries.get(f"{teamCountry}", f"{teamCountry}")
  if country_code == teamCountry:
    flag = f":{country_code.lower()}:"
  else:
    flag = f":flag_{country_code.lower()}:"
  team_embed = discord.Embed(color=32222)
  team_embed.set_author(name=f"{TeamName} - {teamLeague}", icon_url=logo_url)
  team_embed.add_field(name=":earth_americas: Country", value=f"{flag} {teamCountry}")
  team_embed.add_field(name="📝 Record", value=f"{teamRecord}")
  team_embed.add_field(name="🧑‍💼 Manager", value=f"{teamManager}")
  team_embed.add_field(name=":soccer: Total Goals", value=f"{teamGoals_scored}")
  team_embed.add_field(name="🛒 Points ", value=f"{teamPoints}")
  team_embed.add_field(name="1️⃣ Position ", value=f"{teamPosition}")
  team_embed.add_field(name="🏆 League ", value=f"{teamLeague}")
  team_embed.add_field(name="🧑 Gender ", value=f"{teamGender}")
  team_embed.add_field(name="⚽ Expected Goals ", value=f"{teamExpected_goals}")
  team_embed.timestamp = datetime.now()
  team_embed.set_footer(text="By Diveer#0001", icon_url="https://cdn.discordapp.com/avatars/980248087983456347/a308e85351b96b12ad28b47ebd5682e7.webp?size=160")
  await ctx.send(embed=team_embed)







client.run("OTgwMjQ4MDg3OTgzNDU2MzQ3.GasG2v.u2OvvHCtovGJ-NB8sBQxriYpBiPoU0Ka2UNnLQ")