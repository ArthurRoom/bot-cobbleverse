import discord
from discord.ext import commands
import aiohttp

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dex")
    async def dex(self, ctx, pokemon: str):
        pokemon = pokemon.lower()
        
        async with aiohttp.ClientSession() as session:
            url_poke = f"https://pokeapi.co/api/v2/pokemon/{pokemon}"
            async with session.get(url_poke) as resp:
                if resp.status != 200:
                    return await ctx.send(f"❌ Pokémon `{pokemon}` não encontrado!")
                data = await resp.json()

            url_species = data['species']['url']
            async with session.get(url_species) as resp:
                spec_data = await resp.json()
            
            evo_url = spec_data['evolution_chain']['url']
            async with session.get(evo_url) as resp:
                evo_data = await resp.json()

            # --- LÓGICA DE LINHA EVOLUTIVA ---
            def montar_linha_evolutiva(current_chain):
                if not current_chain['evolves_to']: return []
                todas_evos = []
                for next_step in current_chain['evolves_to']:
                    poke_nome = next_step['species']['name'].capitalize()
                    details = next_step['evolution_details'][0]
                    metodo = ""
                    trigger = details['trigger']['name']
                    if trigger == 'level-up':
                        if details.get('min_level'): metodo = f" (Nvl {details['min_level']})"
                        elif details.get('min_happiness'): metodo = " (Felicidade)"
                        else: metodo = " (Especial/Nvl)"
                    elif trigger == 'use-item':
                        item = details['item']['name'].replace('-', ' ').capitalize()
                        metodo = f" (Usar {item})"
                    elif trigger == 'trade': metodo = " (Troca)"
                    
                    todas_evos.append(f"• {poke_nome}{metodo}")
                    sub_evos = montar_linha_evolutiva(next_step)
                    for sub in sub_evos: todas_evos.append(f"  └ {sub}")
                return todas_evos

            def achar_ponto_na_cadeia(current_chain, target_name):
                if current_chain['species']['name'] == target_name: return current_chain
                for next_evo in current_chain['evolves_to']:
                    res = achar_ponto_na_cadeia(next_evo, target_name)
                    if res: return res
                return None

            ponto_atual = achar_ponto_na_cadeia(evo_data['chain'], pokemon)
            lista_final = montar_linha_evolutiva(ponto_atual) if ponto_atual else []
            exibicao_evo = "\n".join(lista_final) if lista_final else "Forma Final"

            # --- STATUS BASE ---
            stats = {}
            for s in data['stats']:
                name = s['stat']['name']
                value = s['base_stat']
                stats[name] = value

            # Tradução e Formatação dos Status
            status_formatado = (
                f"❤️ **HP:** {stats['hp']}\n"
                f"⚔️ **ATK:** {stats['attack']} | **SPA:** {stats['special-attack']}\n"
                f"🛡️ **DEF:** {stats['defense']} | **SPD:** {stats['special-defense']}\n"
                f"⚡ **SPE:** {stats['speed']}"
            )

            # --- DADOS GERAIS ---
            habs = ", ".join([h['ability']['name'].replace('-', ' ').capitalize() for h in data['abilities']])
            tipos = " / ".join([t['type']['name'].capitalize() for t in data['types']])
            imagem = data['sprites']['other']['official-artwork']['front_default']

            # --- EMBED ---
            embed = discord.Embed(title=f"#{data['id']} - {data['name'].capitalize()}", color=0x3B4CCA)
            embed.set_thumbnail(url=imagem)
            
            # Campos organizados
            embed.add_field(name="🧬 Evoluções", value=f"```text\n{exibicao_evo}\n```", inline=False)
            embed.add_field(name="📊 Status Base", value=status_formatado, inline=True)
            embed.add_field(name="✨ Infos", value=f"**Tipo:** {tipos}\n**Habs:** {habs}", inline=True)
            
            # Spawns (Adicione mais aqui)
            spawns = {"gastly": "🌑 Pântanos/Cemitérios", "gengar": "🌑 Estruturas à Noite"}
            embed.add_field(name="📍 Onde Encontrar", value=spawns.get(pokemon, "❓ Biomas padrão do mod."), inline=False)

            embed.set_footer(text=f"Consultado por {ctx.author.name} | Pokédex do Santuário")

            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Wiki(bot))