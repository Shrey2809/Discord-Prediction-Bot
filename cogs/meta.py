import discord 
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = discord.Embed(
            description="**Reaction Poll**\nCreate a reaction poll with multiple options by typing `+poll {title} [Option1] [Option2] [Option3]`.",
            colour=0x83BAE3,
        )

    @commands.command(name="help")
    @commands.cooldown(2,60,BucketType.user) 
    async def help(self, ctx):
        await ctx.message.channel.send(embed=self.help_message)

def setup(bot):
    bot.add_cog(Meta(bot))
