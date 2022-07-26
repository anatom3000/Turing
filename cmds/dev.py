import discord
from discord.ext import commands

import json

class Developper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def config(self, ctx):
        await ctx.send(":no_entry_sign: You must provide a subcommand (`save` or `reload`)")


    @config.command(name="reload")
    async def config_reload(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return await ctx.send(":no_entry_sign: You need to be the owner to do that!")
        async with ctx.message.channel.typing():
            with open(self.bot.CONFIG_PATH, mode='r') as f:
                self.bot.config = json.load(f)
        await ctx.send(":white_check_mark: Reloaded configuration!")

    @config.command(name="save")
    async def config_save(self, ctx):
        if await self.bot.is_owner(ctx.author):
            return await ctx.send(":no_entry_sign: You need to be a moderator to do that!")
        async with ctx.message.channel.typing():
            with open(self.bot.CONFIG_PATH, mode='w') as f:
                json.dump(self.bot.config, f, indent=4)
        await ctx.send(":white_check_mark: Saved configuration!")

    @commands.group(invoke_without_command=True)
    async def ext(self, ctx):
        await ctx.send(":no_entry_sign: You must provide a subcommand (`reload` or `add`)")


    @ext.command(name="reload")
    async def ext_reload(self, ctx, extension: str = None):
        print(await self.bot.is_owner(ctx.author))
        if await self.bot.is_owner(ctx.author):
            return await ctx.send(":no_entry_sign: You need to be the owner to do that!")
        if extension is None:
            for ext in self.bot.extensions.keys():
                try:
                    self.bot.reload_extension(ext)
                except Exception as err:
                    return await ctx.send(f":no_entry_sign: An error occured while trying to load `{ext}`.\n`{err.__class__.__name__}: {err}`")
            return await ctx.send(f":white_check_mark: Successfully reloaded all extensions !")
        try:
            self.bot.reload_extension(extension)
        except Exception as err:
            return await ctx.send(f":no_entry_sign: An error occured while trying to load `{extension}`.\n`{err.__class__.__name__}: {err}`")
        await ctx.send(f"Successfully reloaded `{extension}` !")

    @ext.command(name="add")
    async def ext_add(self, ctx, extension: str):
        if await self.bot.is_owner(ctx.author):
            return await ctx.send(":no_entry_sign: You need to be the owner to do that!")
        try:
            self.bot.load_extension(extension)
            self.bot.loaded_extensions.append(extension)
        except Exception as err:
            return await ctx.send(f":no_entry_sign: An error occured while trying to load `{extension}`.\n`{err.__class__.__name__}: {err}`")
        await ctx.send(f":white_check_mark: Successfully added `{extension}` !")

    @commands.command()
    async def logging(self, ctx, state: bool = None):
        if ctx.author.id != self.bot.config["owner"]:
            return await ctx.send(":no_entry_sign: You need to be the owner to do that!")
        if state is None:
            self.bot.config["logging"] = not self.bot.config["logging"]
        else:
            self.bot.config["logging"] = state
        await ctx.send(f":white_check_mark: Message ~~spying~~ logging is now {'ON' if self.bot.config['logging'] else 'OFF'}!")

def setup(bot): 
    bot.add_cog(Developper(bot))