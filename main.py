import discord
import os
import asyncio
import datetime
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- 1. FUNÇÃO DE CARREGAMENTO (Mantenha como estava) ---
async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

# --- 2. O AVISO DE DESLIGAMENTO (Cole antes do main) ---
async def notify_shutdown():

    LOG_CHANNEL_ID = 1491528102793445598 
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        try:
            # Enviamos a mensagem e esperarmos ela chegar
            await channel.send(f"🔴 **[SISTEMA OFF]** O bot foi desligado às `{timestamp}`.")
        except:
            pass

# --- 3. A LÓGICA PRINCIPAL (Ajustada) ---
async def main():
    async with bot:
        await load_extensions()
        try:
            await bot.start(TOKEN)
        except KeyboardInterrupt:
            # Quando você der Ctrl+C, ele executa o aviso antes de fechar
            await notify_shutdown()
            await bot.close()

@tasks.loop(minutes=5) # Muda a cada 5 minutos
async def status_task():
    await bot.change_presence(activity=discord.Game(name="Jogando Cobbleverse 🐉"))
    await asyncio.sleep(150) # Espera um pouco
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Assistindo o Tutupadinha no YT"))

# Inicia a tarefa quando o bot liga
@bot.event
async def on_ready():
    status_task.start()
    print(f'✅ Sistema Tutupadinha iniciado!')
    print("✅ Status rotativo iniciado!")

# --- 4. O DISPARADOR (Fica no final de tudo) ---
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Garante que o terminal não jogue um erro feio na tela
        print("\nProcesso finalizado pelo Tutupadinha.")