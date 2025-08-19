import os
import discord
from discord.ext import commands
from canvas_api import get_upcoming_assignments
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# print upcoming assignments
@bot.command(name="assignments")
async def assignments(ctx):
    data = get_upcoming_assignments()
    if not data:
        await ctx.send("No upcoming assignments found.")
        return
    msg = "\n".join([f"{a['context_name']}: {a['title']} (due {a['due_at']})" for a in data])
    await ctx.send(msg)

bot.run(DISCORD_TOKEN)