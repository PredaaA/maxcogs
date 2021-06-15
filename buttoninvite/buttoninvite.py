import discord
from dislash.interactions import ActionRow, Button, ButtonStyle
from redbot.core import Config, commands


class ButtonInvite(commands.Cog):
    """Sends the invite for [botname] with button.

    To set permission level use `[p]inviteset perms`, and you can change description by using `[p]invmsg`."""

    __author__ = "MAX"
    __version__ = "0.2.0a"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad!"""
        pre_processed = super().format_help_for_context(ctx)
        return f"{pre_processed}\n\nAuthor: {self.__author__}\nCog Version: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("invite")
        self.config = Config.get_conf(self, identifier=12435434124)
        self.def_msg = "Thank you for inviting {}\n\n**Click on the button!**"
        self.config.register_global(msg=self.def_msg)

    @commands.is_owner()
    @commands.group()
    async def invmsg(self, ctx):
        """Settings to change invite message shown in the embed."""

    @invmsg.command()
    async def add(self, ctx, *, message):
        """Change the invite message shown in the embed."""
        if message:
            await self.config.msg.set(message)
            await ctx.send(f"Sucessfully set the invite message")

    @invmsg.command()
    async def reset(self, ctx, *, message=None):
        """Reset the invite message back to default."""
        await self.config.msg.set(self.def_msg)
        await ctx.send(f"Reset the invite message back to default")

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def invite(self, ctx):
        """Shows [botname]'s invite link.

        To set permission level use `[p]inviteset perms`.
        You can change description by using `[p]invmsg`."""

        servers = str(len(self.bot.guilds))
        name = ctx.bot.user.name

        embed = discord.Embed(
            title=f"{name}",
            colour=discord.Colour(0x5865F2),
            url=(ctx.bot.user.avatar_url_as(static_format="png")),
            description=(await self.config.msg()).format(name),
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar_url_as(static_format="png"))
        embed.set_footer(text=f"Server count: {servers}")
        await ctx.send(
            embed=embed,
            components=[
                ActionRow(
                    Button(
                        style=ButtonStyle.link,
                        label="Invite me",
                        url=(await self.bot.get_cog("Core")._invite_url()),
                    ),
                )
            ],
        )
