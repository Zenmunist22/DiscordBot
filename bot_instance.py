from discord.ext import commands
from discord import Intents, Client, Message
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
