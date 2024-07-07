import discord
from discord.ext import commands
from ...utils import utils
from ... import config

sniped_messages: dict = {}

def get_snipe_embed(message: str, channel: discord.TextChannel, ctx: commands.Context) -> discord.Embed:
  embed: discord.Embed = discord.Embed(color = discord.Color.purple())
  embed.set_author(name=f"Last Deleted Message In {channel.name}")
  embed.add_field(name="Author:", value=message.author.mention)
  embed.add_field(name="Message:", value=message.content)
  embed.timestamp = message.created_at
  embed.set_footer(text=f"{config.SERVER_NAME}", icon_url=f"{config.SERVER_ICON}")
  
  # Handle The Avatar For The Member Profile
  if ctx.author.avatar == None:
    avatar: str = "https://cdn.discordapp.com/embed/avatars/0.png"
    embed.set_author(name=f"{ctx.author.name}", icon_url=f"{avatar}")
  else:
    embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar}")
  return embed

class snipe(commands.Cog):
  def __init__(self, bot: discord.Bot):
    self.bot: discord.Bot = bot

  @commands.Cog.listener()
  async def on_message_delete(self, message):
    if len(sniped_messages) == 3:
      del sniped_messages[-1]
    history = sniped_messages.get(message.channel.id, [])
    history.insert(0, message)
    sniped_messages[message.channel.id] = history

  @commands.command(
    name='snipe',
    aliases=['se', 'deletedmsg'],
  )
  async def snipe_with_prefix(self, ctx: commands.Context, *, page: int = 1) -> None:
    if not utils.check_staff(ctx, ctx.author):
      await ctx.reply('❎ | You are not allowed to use snipe.')
      return False
    
    channel: discord.TextChannel = ctx.channel
    try:
      message = sniped_messages[channel.id][page-1]
    except Exception as e:
      await ctx.channel.send(f"No available snips at page : {page}")
      return
    
    await ctx.send(embed=get_snipe_embed(message, channel, ctx))
  
  @commands.slash_command(guild_ids=[config.SERVER_ID],guild_only=True, name='snipe', description='Get The `n` Deleted Message.')
  async def snipe_with_slash(
    self, 
    ctx: discord.ApplicationContext,
    page: discord.Option(int, name='page', description='The Page To Get The Message From.', default=1),
    visible: discord.Option(bool, name='visible', description='Show the Message For Everyone?', default=False),
  ) -> None:
    if not utils.check_staff(ctx, ctx.author):
      await ctx.send_response(content='❎ | You are not allowed to use snipe.')
      return False
    
    channel: discord.TextChannel = ctx.channel
    try:
      message = sniped_messages[channel.id][page-1]
    except Exception as e:
      await ctx.send_response(ephemeral=not visible, content=f"No available snips at page : {page}")
      return
    
    await ctx.send_response(ephemeral=visible, embed=get_snipe_embed(message, channel, ctx))

def setup(bot):
  bot.add_cog(snipe(bot))
