from typing import Final
import os
import discord
from dotenv import load_dotenv
from discord import Intents, Client, Message

from discord.ext import commands


load_dotenv()
TOKEN: Final[str] = os.getenv('token')

from bot_instance import bot  


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
import menu

def main():  
    bot.run(token=TOKEN)

if __name__ == '__main__':
    main()
