import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ALLOWED_CHANNEL_ID = int(os.getenv('GOOD_MORNING_SALLON_ID'))
if not TOKEN:
    print("❌ DISCORD_TOKEN non trouvé")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def ask_ollama(user_text: str) -> str:
    response = chat(
        model="gpt-oss:20b-cloud",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es mon assistant Meta-Lead. "
                    "Tu aides à clarifier les idées, prioriser, "
                    "et proposer UNE action simple."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response['message']['content']


@bot.event
async def on_ready():
    print(f'✅ {bot.user} est connecté !')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    content = message.content.strip()

    if content.lower().startswith("checkin"):
        user_text = content[len("checkin"):].strip()

        reply = ask_ollama(user_text)
        await message.channel.send(reply)

    await bot.process_commands(message)


bot.run(TOKEN)
