import discord
from discord.ext import commands
import asyncio
import random

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="postar_cargos")
    @commands.has_permissions(administrator=True)
    async def postar_cargos(self, ctx):
        embed = discord.Embed(
            title="🎭 Central de Cargos - Santuário de Kanto",
            description=(
                "Reaja aos emojis abaixo para receber notificações específicas:\n\n"
                "🎉 - **Sorteios**\n"
                "📢 - **Anúncios Gerais**\n"
                "💰 - **Mercado / Trade**\n"
                "⚔️ - **Raids**\n"
                "📅 - **Eventos**"
            ),
            color=0x3B4CCA
        )
        msg = await ctx.send(embed=embed)

        # O bot reage automaticamente na ordem certa
        await msg.add_reaction("🎉")
        await msg.add_reaction("📢")
        await msg.add_reaction("💰")
        await msg.add_reaction("⚔️")
        await msg.add_reaction("📅")

        # O bot printa o ID da mensagem no terminal para você copiar e colar no roles.py
        print(f"ID da mensagem de cargos: {msg.id}")
        await ctx.send(f"✅ Painel postado! O ID da mensagem é: `{msg.id}`)", delete_after=10)

    @commands.command(name="anuncio")
    @commands.has_permissions(administrator=True)
    async def anuncio(self, ctx, canal: discord.TextChannel, *, mensagem):
        # Criamos o Embed normalmente
        embed = discord.Embed(
            title="📢 Anúncio do Santuário",
            description=mensagem,
            color=0x3B4CCA
        )
        embed.set_footer(text=f"Enviado por {ctx.author.name}")
        
        # Aqui está o segredo: enviamos o @everyone FORA do embed
        # O 'content' é o que faz o celular da galera apitar
        await canal.send(content=f"<@&1491546089432682496>", embed=embed) 
        
        await ctx.send(f"✅ Anúncio enviado com ping de everyone em {canal.mention}")

    @commands.command(name="sorteio")
    @commands.has_permissions(administrator=True)
    async def sorteio(self, ctx, tempo: int, *, premio: str):
        embed = discord.Embed(
            title="🎉 SORTEIO INICIADO!",
            description=f"Prêmio: **{premio}**\nReaja com 🎉 para participar!\nTempo: {tempo} segundos",
            color=0x00FF00
        )
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🎉")

        await asyncio.sleep(tempo)

        nova_msg = await ctx.channel.fetch_message(msg.id)
        usuarios = [user async for user in nova_msg.reactions[0].users() if not user.bot]

        if len(usuarios) > 0:
            ganhador = random.choice(usuarios)
            await ctx.send(f"🎊 Parabéns {ganhador.mention}! Você ganhou: **{premio}**!")
        else:
            await ctx.send("😔 Ninguém participou do sorteio.")

async def setup(bot):
    await bot.add_cog(Social(bot))