import os
import discord
from discord.ext import commands
from discord import app_commands
import time
from keep_alive import keep_alive

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

cooldowns = {}
COOLDOWN_TIME = 300

SUPPORT_SERVER = "https://discord.gg/YOUR_INVITE"
BOT_INVITE = "https://discord.com/oauth2/authorize?client_id=YOUR_ID&permissions=0&scope=bot%20applications.commands"

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

async def send_anon(interaction, title, message):
    uid = interaction.user.id
    now = time.time()

    if uid in cooldowns and now - cooldowns[uid] < COOLDOWN_TIME:
        await interaction.response.send_message(
            "⏳ Please wait before sending another message.",
            ephemeral=True
        )
        return

    cooldowns[uid] = now

    embed = discord.Embed(
        title=title,
        description=message,
        color=discord.Color.dark_purple()
    )
    embed.set_footer(text="Anonymous Submission")

    await interaction.response.send_message("✅ Sent anonymously!", ephemeral=True)
    await interaction.channel.send(embed=embed)

@bot.tree.command(name="confess", description="Send an anonymous confession")
async def confess(interaction: discord.Interaction, message: str):
    await send_anon(interaction, "🤫 Anonymous Confession", message)

@bot.tree.command(name="crush", description="Send an anonymous crush")
async def crush(interaction: discord.Interaction, message: str):
    await send_anon(interaction, "💌 Anonymous Crush", message)

@bot.tree.command(name="rant", description="Send an anonymous rant")
async def rant(interaction: discord.Interaction, message: str):
    await send_anon(interaction, "😡 Anonymous Rant", message)

@bot.tree.command(name="joke", description="Send an anonymous joke")
async def joke(interaction: discord.Interaction, message: str):
    await send_anon(interaction, "😂 Anonymous Joke", message)

@bot.tree.command(name="about", description="About the bot")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤫 Anonymous Fun Bot",
        description="Confessions, rants, crushes & jokes — 100% anonymous.",
        color=discord.Color.dark_purple()
    )
    embed.add_field(name="Developer", value="ADAN", inline=False)
    embed.add_field(name="Support Server", value=SUPPORT_SERVER, inline=False)
    embed.add_field(name="Invite Bot", value=BOT_INVITE, inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

keep_alive()
bot.run(TOKEN)
