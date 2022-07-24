import discord
from discord.ext import commands

import openai

class AI(commands.Cog):
    OPEN_AI_PARAMETERS = [
        ('temperature', "The randomness of the answer - Range: 0.0 => 1.0"),
        ('max_tokens', 'The limit of tokens the AI can generate'),
        ('engine', "The model used"),
        ('top_p', "The diversity of the answer - Range: 0.0 => 1.0"),
        ('frequency_penalty', "How likely is the AI to NOT repeat the question - Range: 0.0 => 1.0"),
        ('presence_penalty', "How likely is the AI to talk about new subjects - Range: 0.0 => 1.0")
    ]

    def __init__(self, bot): 
        self.bot = bot
        openai.api_key = self.bot.config["secrets"]["openai"]


    @commands.group(brief="Ask anything to the bot", description="Ask anything to the bot, by using OpenAI technology. Does not know anything about the context.", invoke_without_command=True)
    async def ask(self, ctx, *, question: str):
        async with ctx.message.channel.typing():
            question = question + '\n'
            response = openai.Completion.create(prompt=question,
                                                stop=[";"],
                                                **self.bot.config["ai"]
                                                )
            text = "\n".join(
                filter(lambda x: x != "",
                       response["choices"][0]["text"].strip().split("\n")))
        embed = discord.Embed(
            title=question[0].upper()+question[1:],
            description=text,
        )
        embed.set_footer(text=f"Asked by {ctx.author.display_name}",
                         icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @ask.command()
    async def config(self, ctx, option: str = None, value=None):
        if ctx.author.id != self.bot.config["owner"]:
            return await ctx.send(":no_entry_sign: You need to be the owner to do that!")
        
        if option is None:
            msg = []
            for param in self.OPEN_AI_PARAMETERS:
                msg.append(f"`{param[0]}`: `{self.bot.config['ai'][param[0]]}` - {param[1]}")
            return await ctx.send(embed=discord.Embed(title="Ask command configuration", description='\n'.join(msg)))

        if option not in list(zip(*self.OPEN_AI_PARAMETERS))[0]:
            return await ctx.send(f":no_entry_sign: Invalid option `{option}`")
        
        if value is None:
            return await ctx.send(f":white_check_mark: `{option}` is set to `{self.bot.config['ai'][option]}`")

        try:
            self.bot.config['ai'][option] = type(self.bot.config['ai'][option])(value)
        except ValueError:
            return await ctx.send(f":no_entry_sign: Invalid value: `{value}`")
        await ctx.send(f":white_check_mark: Set `{option}` to `{value}!`")

def setup(bot): # this is called by Pycord to setup the cog
    bot.add_cog(AI(bot)) # add the cog to the bot