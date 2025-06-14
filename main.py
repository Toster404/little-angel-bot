import logging
import discord

from modules.configuration import config

_log = logging.getLogger(__name__)

# Discord Bot
from classes.bot import bot


@bot.event
async def on_ready():

    _log.info(f"Бот запущен как {bot.user}")

    log_channel = bot.get_channel(int(config.BOT_LOGS_CHANNEL_ID.get_secret_value()))
    if log_channel:
        await log_channel.send(embed=discord.Embed(description=f"☑️ Бот запущен как **{bot.user}**", color=config.LITTLE_ANGEL_COLOR))

if __name__ == '__main__':
    # Запуск
    bot.run(config.DISCORD_TOKEN.get_secret_value())
