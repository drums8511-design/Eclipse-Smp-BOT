import os
import discord
from discord.ext import tasks
from mcstatus import JavaServer

TOKEN = os.getenv("TOKEN")

SERVER_IP = "eclipsesmp-v8RC.aternos.me"

CHANNEL_ID = 123456789012345678

bot = discord.Client(
    intents=discord.Intents.default()
)

last_status = None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_server.start()


@tasks.loop(seconds=60)
async def check_server():
    global last_status

    channel = bot.get_channel(CHANNEL_ID)

    if channel is None:
        return

    try:
        server = JavaServer.lookup(SERVER_IP)
        status = server.status()

        message = (
            "🟢 **Eclipse SMP is ONLINE**\n"
            f"👥 Players: {status.players.online}/{status.players.max}\n"
            f"⚔️ Version: {status.version.name}"
        )

    except:
        message = "🔴 **Eclipse SMP is OFFLINE**"


    if message != last_status:
        await channel.send(message)
        last_status = message


bot.run(TOKEN)
