import discord

from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Pong!")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong! 🏓")

async def setup(bot):
    await bot.add_cog(Ping(bot))