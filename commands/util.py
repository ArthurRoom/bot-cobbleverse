import discord
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Remove o comando de help padrão do Discord para usarmos o nosso
        self.bot.remove_command('help')

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="📖 Guia de Comandos - Tutupadinha Bot",
            description="Bem-vindo ao Santuário! Aqui estão os comandos disponíveis para te ajudar na sua jornada Pokémon.",
            color=0x3B4CCA
        )

        # Seção de Pokémon
        embed.add_field(
            name="🐉 Pokémon & Wiki",
            value=(
                "`!dex <nome>` - Wiki com status, evoluções e biomas.\n"
                "`!help` - Mostra esta lista de ajuda."
            ),
            inline=False
        )

        # Seção do Servidor Cobbleverse
        embed.add_field(
            name="🖥️ Servidor",
            value=(
                "`!ip` - Mostra o endereço para conexão.\n"
                "`!status` - Verifica se o servidor está online agora."
            ),
            inline=False
        )

        # Seção de Notificações
        embed.add_field(
            name="🎭 Cargos & Avisos",
            value="Reaja na mensagem oficial no canal de cargos para receber pings de Sorteios, Raids e Trocas!",
            inline=False
        )

        # Seção de Links & Social
        embed.add_field(
            name="📱 Social",
            value=(
                "🎥 [Canal Tutupadinha](https://www.youtube.com/@tutupadinha)\n"
                "🔗 [Discord do Servidor](https://discord.gg/XTJ3TNGaHc)"
            ),
            inline=False
        )

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="Dúvidas? Fale com um Ajudante ou Mod do Santuário.")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Util(bot))