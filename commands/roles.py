import discord
from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # ID da mensagem onde as pessoas vão reagir
        # (Você pega esse ID clicando com o botão direito na mensagem no Discord)
        self.MENSAGEM_REACAO_ID = 1491550397566025832

        # MAPEAMENTO DE EMOJIS PARA CARGOS
        # Formato: "Emoji": ID_DO_CARGO
        self.CARGOS_MAPEADOS = {
            "🎉": 1491546007455137975,  # Cargo de Sorteios
            "📢": 1491546089432682496,  # Cargo de Anúncios
            "💰": 1491546140397666344,  # Cargo de Trade/Mercado
            "⚔️": 1491546242893742263,  # Cargo de Raids
            "📅": 1491546271540842567   # Cargo de Eventos
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # 1. Verifica se a reação foi na mensagem certa
        if payload.message_id != self.MENSAGEM_REACAO_ID:
            return

        # 2. Verifica se o emoji está no nosso dicionário
        emoji_recebido = str(payload.emoji)
        if emoji_recebido in self.CARGOS_MAPEADOS:
            guild = self.bot.get_guild(payload.guild_id)
            cargo_id = self.CARGOS_MAPEADOS[emoji_recebido]
            role = guild.get_role(cargo_id)

            if role:
                member = guild.get_member(payload.user_id)
                if member and not member.bot:
                    await member.add_roles(role)
                    try:
                        # Avisa no privado para o user ter certeza que funcionou
                        await member.send(f"✅ Você agora tem o cargo **{role.name}** no Santuário!")
                    except:
                        pass # Se o DM for fechado, o bot não crasha

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Mesma lógica, mas para remover o cargo
        if payload.message_id == self.MENSAGEM_REACAO_ID:
            emoji_recebido = str(payload.emoji)
            if emoji_recebido in self.CARGOS_MAPEADOS:
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(self.CARGOS_MAPEADOS[emoji_recebido])
                member = guild.get_member(payload.user_id)

                if member and role:
                    await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(Roles(bot))