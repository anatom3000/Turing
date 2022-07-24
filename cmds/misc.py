import discord
from discord.ext import commands

class Miscellaneous(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot
        self.repeat = True

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot ready, logged in as {self.bot.user}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and self.bot.config["parrot_mode"]:
            await message.channel.send(message.content)
            await message.delete()
        if self.bot.config["logging"]:
            print(f"[{message.channel}] {message.author}: {message.content}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Bonk in {round(self.bot.latency*1000)}ms!")

    @commands.command()
    async def about(self, ctx):
        owner = await self.bot.fetch_user(self.bot.config["owner"])
        await ctx.send(f"`{self.bot.user.name} v{self.bot.__version__}` - Made by `{owner.name}#{owner.discriminator}`")

    @commands.command()
    async def fuck(self, ctx, target = "you"):
        if "you" in target:
            return await ctx.send("no u")
        else:
            return await ctx.send(f":white_check_mark: Fucked {target}! :+1:")

    @commands.command()
    async def parrot_mode(self, ctx, state: bool = None):
        if ctx.author.id not in self.bot.config["moderators"]:
            return await ctx.send(":no_entry_sign: You need to be a moderator to do that!")
        if state is None:
            self.bot.config["parrot_mode"] = not self.bot.config["parrot_mode"]
        else:
            self.bot.config["parrot_mode"] = state
        await ctx.send(f":white_check_mark: Bot repeat is now {'ON' if self.bot.config['parrot_mode'] else 'OFF'}! Have fun! :smirk:")

    @commands.command(hidden=True)
    async def cheh(self, ctx):
        if ctx.author.id not in self.bot.config["moderators"]:
            return await ctx.send(":no_entry_sign: You need to be a moderator to do that!")
        await ctx.send("Cheh ! (T'as le seum hein ?!!!)")
        await ctx.message.delete()

    @commands.command()
    async def rickroll(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")



def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(Miscellaneous(bot)) # add the cog to the bot