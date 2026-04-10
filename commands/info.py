import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ip(self, ctx):
        await ctx.send('🎮 O IP do servidor é: `santuariodekanto.enxada.host`')

    @commands.command()
    async def status(self, ctx):
        await ctx.send('🛰️ O servidor está online e estável!')

async def setup(bot):
    await bot.add_cog(Info(bot))