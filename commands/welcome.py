import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.CARGO_INICIAL_ID = 1484670397109506128

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # --- PARTE 1: DAR O CARGO ---
        role = member.guild.get_role(self.CARGO_INICIAL_ID)
        if role:
            try:
                await member.add_roles(role)
                print(f"✅ Cargo {role.name} entregue para {member.name}")
            except discord.Forbidden:
                print(f"❌ Erro: O bot não tem permissão para dar o cargo {role.name}. Verifique a hierarquia!")
        
        # --- PARTE 2: ENVIAR O EMBED (Seu código anterior) ---
        channel = discord.utils.get(member.guild.text_channels, name="🏠-bem-vindo")
        if channel:
            embed = discord.Embed(
                title="🏛️ BEM-VINDO AO SANTUÁRIO DE KANTO 🏛️",
                description=f"Vá direto ler as <#{1484249769873506466}>\nAproveite e desfrute do nosso Servidor!",
                color=0x005bb7
            )
            embed.set_author(name="Tutupadinha")
            await channel.send(content=f"Bem-vindo {member.mention} ao **Santuário de Kanto**!", embed=embed)

    @commands.command()
    async def testebv(self, ctx):
        # O comando de teste continua igual, apenas para ver o visual
        await self.on_member_join(ctx.author)

async def setup(bot):
    await bot.add_cog(Welcome(bot))

    # Comando para testar se o visual está ok
    @commands.command()
    async def testebv(self, ctx):
        member = ctx.author
        channel = discord.utils.get(member.guild.text_channels, name="bot-log")
        
        if channel:
            embed = discord.Embed(
                title="🏛️ BEM-VINDO AO SANTUÁRIO DE KANTO 🏛️",
                description=f"Vá direto ler as <#{1484249769873506466}>\nAproveite e Desfrute do nosso Servidor!",
                color=0x005bb7
            )
            embed.set_author(name="Tutupadinha")
            
            await channel.send(content=f"Bem-vindo {member.mention} ao **Santuário de Kanto**!", embed=embed)
        else:
            await ctx.send("❌ Canal `bem-vindo` não encontrado.")

# Função obrigatória para o main.py conseguir carregar este arquivo
async def setup(bot):
    await bot.add_cog(Welcome(bot))