import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

COR = 0x2b6fff
IMAGEM = "https://cdn.discordapp.com/attachments/1497779438157434971/1497779484047446176/ChatGPT_Image_25_de_abr._de_2026_22_50_24.png"


@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

    print(f"Bot online como {bot.user}")


@bot.command()
async def regras(ctx):
    embed = discord.Embed(
        title="Regras do Servidor",
        description="Para manter a organização e o bom funcionamento, siga as diretrizes abaixo:",
        color=COR
    )
    embed.set_image(url=IMAGEM)
    embed.add_field(name="📌 Regras Gerais",
                    value="• Respeito entre todos\n• Proibido spam/divulgação\n• Utilize os canais corretamente\n• Sem conteúdo ofensivo",
                    inline=False)
    embed.add_field(name="⚠️ Importante",
                    value="O não cumprimento das regras pode resultar em punições.",
                    inline=False)
    embed.set_footer(text="Aura Layouts • Servidores profissionais")

    await ctx.send(embed=embed)


@bot.command()
async def planos(ctx):
    embed = discord.Embed(
        title="Nossos Planos",
        description="Servidores personalizados com estrutura profissional.",
        color=COR
    )
    embed.set_image(url=IMAGEM)
    embed.add_field(name="🔹 Básico", value="• Estrutura organizada\n• Canais essenciais\n• Entrega rápida", inline=False)
    embed.add_field(name="🔸 Intermediário", value="• Design personalizado\n• Organização avançada\n• Ajustes básicos", inline=False)
    embed.add_field(name="🔻 Premium", value="• Servidor completo\n• Identidade visual exclusiva\n• Suporte pós-entrega", inline=False)
    embed.set_footer(text="Aura Layouts • Servidores profissionais")

    await ctx.send(embed=embed)


@bot.command()
async def portfolio(ctx):
    embed = discord.Embed(
        title="Portfólio",
        description="Projetos já realizados.",
        color=COR
    )
    embed.set_image(url=IMAGEM)
    embed.add_field(name="Projetos",
                    value="• Servidores de loja\n• Comunidades\n• Estruturas RP\n• Abra um ticket para ver mais exemplos.",
                    inline=False)
    embed.set_footer(text="Aura Layouts • Servidores profissionais")

    await ctx.send(embed=embed)


@bot.command()
async def diferenciais(ctx):
    embed = discord.Embed(
        title="Diferenciais",
        description="Por que escolher nosso serviço:",
        color=COR
    )
    embed.set_image(url=IMAGEM)
    embed.add_field(name="Vantagens",
                    value="• Estrutura profissional\n• Design moderno\n• Entrega rápida\n• Fácil utilização",
                    inline=False)
    embed.set_footer(text="Aura Layouts • Servidores profissionais")

    await ctx.send(embed=embed)


@bot.command()
async def como(ctx):
    embed = discord.Embed(
        title="Como Funciona",
        description="Processo simples e direto.",
        color=COR
    )
    embed.set_image(url=IMAGEM)
    embed.add_field(name="Passo a passo",
                    value="1. Escolha um plano\n2. Entre em contato\n3. Explique seu projeto\n4. Receba seu servidor pronto",
                    inline=False)
    embed.set_footer(text="Aura Layouts • Servidores profissionais")

    await ctx.send(embed=embed)


@bot.command()
async def beneficios(ctx):
    embed = discord.Embed(
        title="Benefícios",
        description="Confira alguns dos benefícios de nossos servidores:",
        color=COR
    )
    embed.set_image(url=IMAGEM)
    embed.add_field(
        name="Benefícios e recompensas",
        value="1. Convide **25 amigos** → plano básico grátis\n"
              "2. Convide **35 amigos** → plano intermediário grátis\n"
              "3. Convide **50 amigos** → plano premium grátis\n"
              "4. Solicite via ticket com prova dos convites.",
        inline=False
    )
    embed.set_footer(text="Aura Layouts • Servidores profissionais")

    await ctx.send(embed=embed)


class MotivoModal(discord.ui.Modal, title="Motivo da Avaliação"):
    motivo = discord.ui.TextInput(
        label="Por que você não ficou satisfeito?",
        style=discord.TextStyle.paragraph,
        placeholder="Explique o motivo...",
        required=True,
        max_length=500
    )

    def __init__(self, atendimento, rapidez, usuario):
        super().__init__()
        self.atendimento = atendimento
        self.rapidez = rapidez
        self.usuario = usuario

    async def on_submit(self, interaction: discord.Interaction):
        geral = (self.atendimento + self.rapidez) / 2

        embed = discord.Embed(
            title="Avaliação ┃ Aura Layouts",
            color=discord.Color.blue()
        )
        embed.set_image(url=IMAGEM)

        embed.add_field(name="👤 Avaliador", value=self.usuario.mention, inline=False)
        embed.add_field(name="💬 Atendimento", value=f"{self.atendimento}/10", inline=True)
        embed.add_field(name="⚡ Rapidez", value=f"{self.rapidez}/10", inline=True)
        embed.add_field(name="⭐ Nota Geral", value=f"{geral:.2f}/10", inline=False)
        embed.add_field(name="❌ Não atendeu expectativa", value=self.motivo.value, inline=False)

        await interaction.response.send_message(embed=embed)


@bot.tree.command(name="avaliar", description="Avalie o atendimento")
@app_commands.describe(
    atendimento="Nota para o atendimento (0 a 10)",
    rapidez="Nota para a rapidez (0 a 10)",
    satisfeito="O serviço atendeu seu pedido?"
)
@app_commands.choices(satisfeito=[
    app_commands.Choice(name="Sim", value="sim"),
    app_commands.Choice(name="Não", value="nao")
])
async def avaliar(interaction: discord.Interaction, atendimento: int, rapidez: int, satisfeito: app_commands.Choice[str]):

    if not (0 <= atendimento <= 10 and 0 <= rapidez <= 10):
        await interaction.response.send_message(
            "❌ As notas devem estar entre 0 e 10.",
            ephemeral=True
        )
        return

    if satisfeito.value == "nao":
        await interaction.response.send_modal(
            MotivoModal(atendimento, rapidez, interaction.user)
        )
        return


    geral = (atendimento + rapidez) / 2

    embed = discord.Embed(
        title="Avaliação ┃ Aura Layouts",
        color=discord.Color.blue()
    )
    embed.set_image(url=IMAGEM)

    embed.add_field(name="👤 Avaliador", value=interaction.user.mention, inline=False)
    embed.add_field(name="💬 Atendimento", value=f"{atendimento}/10", inline=True)
    embed.add_field(name="⚡ Rapidez", value=f"{rapidez}/10", inline=True)
    embed.add_field(name="⭐ Nota Geral", value=f"{geral:.2f}/10", inline=False)
    embed.add_field(name="✅ Atendeu expectativa", value="Sim", inline=False)

    await interaction.response.send_message(embed=embed)


bot.run("MTQ5Nzc3NTE5NTY4MTcyMjM2OA.GYpnHu.YqDzrq3vGWVhYGQUN7RDDEOVGOzPErtjEqsS1E")
