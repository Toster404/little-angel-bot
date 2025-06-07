import typing
import discord
import asyncio

from datetime                  import timedelta, datetime, timezone
from apscheduler.triggers.date import DateTrigger

from discord import app_commands
from discord.ext import commands

from classes.bot       import LittleAngelBot
from classes.database  import db
from classes.scheduler import scheduler

from modules.time_converter import Duration, verbose_timedelta

class AutoRemove(commands.Cog):
    def __init__(self, bot: LittleAngelBot):
        self.bot = bot

    autoremove_group = app_commands.Group(
        name="автоудаление",
        description="Автоматическое удаление чего-либо",
        guild_only=True
    )

    @autoremove_group.command(name="сообщений", description="Автоматически удаляет сообщение через заданное время")
    @app_commands.describe(message_id="Введите ID сообщения для удаления (вы можете удалять только свои без права управления сообщениями)", duration='Укажите время через которое надо удалить сообщение', channel='Выберите канал где размещено сообщение')
    async def autoremove_messages_command(self, interaction: discord.Interaction, message_id: int, duration: app_commands.Transform[str, Duration], channel: typing.Union[discord.TextChannel, discord.Thread, discord.VoiceChannel]=None):
        if not channel:
            channel = interaction.channel
        bot_member = interaction.guild.me
        if not isinstance(channel, typing.Union[discord.TextChannel, discord.Thread, discord.VoiceChannel]):
            return await interaction.response.send_message(embed=discord.Embed(title="❌ Ошибка!", color=0xff0000, description="Команду можно применять только к текстовым каналам, веткам и голосовым каналам!"), ephemeral=True)
        channel_permissions = channel.permissions_for(bot_member)
        if not (channel_permissions.read_messages and channel_permissions.read_message_history):
            return await interaction.response.send_message(embed=discord.Embed(title="❌ Ошибка!", color=0xff0000, description="У бота нет права просматривать указанный канал или просматривать историю его сообщений для использования этой команды!"), ephemeral=True)
        if not channel_permissions.manage_messages:
            return await interaction.response.send_message(embed=discord.Embed(title="❌ Ошибка!", color=0xff0000, description="У бота нет права управлять сообщениями в канале для использования этой команды!"), ephemeral=True)
        try:
            message = await channel.fetch_message(message_id)
        except:
            return await interaction.response.send_message(embed=discord.Embed(title="❌ Ошибка!", color=0xff0000, description="Сообщения с указанным ID не существует!"), ephemeral=True)
        if message.author.id != interaction.user.id and not channel.permissions_for(interaction.user).manage_messages:
            return await interaction.response.send_message(embed=discord.Embed(title="❌ Ошибка!", color=0xff0000, description="Вы не можете удалять чужие сообщения без права на управление сообщениями!"), ephemeral=True)
        if duration > timedelta(days=30) or duration < timedelta(seconds=3):
            return await interaction.response.send_message(embed=discord.Embed(title="❌ Ошибка!", color=0xff0000, description="Вы указали длительность, которая больше, чем 1 месяц, либо меньше, чем 3 секунды!"), ephemeral=True)
        duration_datetime = datetime.now(timezone.utc) + duration
        await interaction.response.send_message(embed=discord.Embed(title="☑️ Принято!", color=0x54ef35, description=f"Бот удалит указанное сообщение через {verbose_timedelta(duration)} (<t:{int(duration_datetime.timestamp())}:D>)"), ephemeral=True)
        scheduler.add_job(message.delete(), trigger=DateTrigger(run_date=duration_datetime))


async def setup(bot: LittleAngelBot):
    await bot.add_cog(AutoRemove(bot))
