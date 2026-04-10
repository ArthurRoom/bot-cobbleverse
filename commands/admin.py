import discord
from discord.ext import commands
import datetime

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.LOG_CHANNEL_ID = 1491528102793445598 

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(self.LOG_CHANNEL_ID)
        if channel:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            await channel.send(f"🟢 **[SISTEMA ON]** O terminal foi conectado às `{timestamp}`.")

    # Comando para enviar algo do Discord para o Terminal do PC
    @commands.command()
    @commands.is_owner()
    async def console(self, ctx, *, mensagem):
        print(f"💬 [DISCORD -> CONSOLE]: {mensagem}")
        await ctx.send(f"✅ Mensagem enviada para o terminal do PC.")

    # Exemplo de Log de Erros: Se um comando der erro, ele avisa no Discord
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        channel = self.bot.get_channel(self.LOG_CHANNEL_ID)
        if channel:
            await channel.send(f"⚠️ **Erro no Comando !{ctx.command}**: ```text\n{error}\n```")

async def setup(bot):
    await bot.add_cog(Admin(bot))