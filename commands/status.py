import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import os

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IP_SERVIDOR = "santuariodekanto.enxada.host" # COLOQUE O SEU IP
        
        # IDs DOS CANAIS DE VOZ (Crie dois e cole os IDs aqui)
        self.CANAL_STATUS_ID = 1491590173136523488 
        self.CANAL_RECORDE_ID = 1491596452919644202 
        
        self.arquivo_recorde = "recorde.txt"
        self.atualizar_status.start()

    def obter_recorde(self):
        if not os.path.exists(self.arquivo_recorde):
            return 0
        with open(self.arquivo_recorde, "r") as f:
            try:
                return int(f.read())
            except:
                return 0

    def salvar_recorde(self, novo_recorde):
        with open(self.arquivo_recorde, "w") as f:
            f.write(str(novo_recorde))

    @tasks.loop(minutes=5) # 5 minutos é um tempo seguro
    async def atualizar_status(self):
        await self.bot.wait_until_ready()
        
        try:
            server = JavaServer.lookup(self.IP_SERVIDOR)
            status = server.status()
            online = status.players.online
            
            # Atualiza Canal de Status
            canal_on = self.bot.get_channel(self.CANAL_STATUS_ID)
            if canal_on:
                await canal_on.edit(name=f"🟢 Online: {online} Players")

            # Lógica do Recorde
            recorde_atual = self.obter_recorde()
            if online > recorde_atual:
                self.salvar_recorde(online)
                recorde_atual = online
            
            # Atualiza Canal de Recorde
            canal_rec = self.bot.get_channel(self.CANAL_RECORDE_ID)
            if canal_rec:
                await canal_rec.edit(name=f"🏆 Recorde: {recorde_atual} On")

        except Exception as e:
            print(f"Erro no status: {e}")
            canal_on = self.bot.get_channel(self.CANAL_STATUS_ID)
            if canal_on:
                await canal_on.edit(name="🔴 Servidor Offline")

async def setup(bot):
    await bot.add_cog(ServerStats(bot))