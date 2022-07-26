import discord
from discord.ext import commands


class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message: str):
        if ctx.author.id not in self.bot.config["moderators"]:
            return await ctx.send(":no_entry_sign: You need to be a moderator to do that!")
        await ctx.send(message)
        await ctx.message.delete()

    @commands.group(invoke_without_command=True)
    async def moderator(self, ctx):
        await ctx.send(":no_entry_sign: You must provide a subcommand! (`add` or `remove`)")


    @moderator.command(name="add")
    async def mod_add(self, ctx, user: discord.Member):
        if ctx.author.id == self.bot.config["owner"]:
            if user.id in self.bot.config["moderators"]:
                return await ctx.send(f":no_entry_sign: `{user.display_name}` is already a moderator!")
            self.bot.config["moderators"].append(user.id)
            return await ctx.send(f":white_check_mark: Added `{user.display_name}` to moderators!")
        await ctx.send(":no_entry_sign: You need to be the owner to do that!")


    @moderator.command(name="remove")
    async def remove_moderator(self, ctx, user: discord.Member):
        if ctx.author.id == self.bot.config["owner"]:
            if user.id not in self.bot.config["moderators"]:
                return await ctx.send(f":no_entry_sign: `{user.nick}` is not a moderator!")
            self.bot.config["moderators"].remove(user.id)
            return await ctx.send(f":white_check_mark: Removed moderator permissions for `{user.display_name}`!")
        await ctx.send(":no_entry_sign: You need to be a moderator to do that!")


def setup(bot):
    bot.add_cog(Administration(bot))