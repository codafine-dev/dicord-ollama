import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from ollama import chat
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ALLOWED_CHANNEL_ID = int(os.getenv('GOOD_MORNING_SALLON_ID'))
LINKS_CHANNEL_ID = int(os.getenv('LINKS_CHANNEL_ID'))
if not TOKEN:
    print("❌ DISCORD_TOKEN non trouvé")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
URL_REGEX = r'https?://\S+'
# buffer temporaire
link_buffer = []
message_buffer = []
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
                    "Sois clair, concis, sans blabla."
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    return response['message']['content']

def extract_links_with_ollama(text: str):
    response = chat(
        model="gpt-oss:20b-cloud",
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract all URLs from the text. "
                    "Return ONLY a plain list of URLs, one per line. "
                    "No explanation."
                    "Only return URLs that are explicitly present in the text. Do not invent anything."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    content = response['message']['content']
    return [line.strip() for line in content.split("\n") if line.strip().startswith("http")]

@bot.event
async def on_ready():
    print(f'✅ {bot.user} est connecté !')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.strip()

    # 👉 TRIGGER
    if "parti" in content.lower():
        source_channel = message.channel
        target_channel = bot.get_channel(LINKS_CHANNEL_ID)

        all_links = []
        messages_to_delete = []

        # 👇 on récupère l’historique (limite ajustable)
        async for msg in source_channel.history(limit=100):
            if msg.author == bot.user:
                continue
            text = msg.content.strip()

            # extraction regex
            urls = re.findall(URL_REGEX, text)

            # fallback ollama
            if not urls and len(text) > 30:
                try:
                    urls = extract_links_with_ollama(text)
                except:
                    urls = []

            if urls:
                for url in urls:
                    entry = f"- {url}"
                    if entry not in all_links:
                        all_links.append(entry)
                set(all_links)  # unique
                messages_to_delete.append(msg)

        # 👉 aucun lien
        if not all_links:
            await message.channel.send("😴 Aucun lien trouvé")
            return

        # 👉 envoi regroupé
        if target_channel:
            grouped_message = "📦 **Liens à traiter :**\n" + "\n".join(all_links)
            await target_channel.send(grouped_message)

        # 👉 suppression
        for msg in messages_to_delete:
            try:
                await msg.delete()
            except Exception as e:
                print("Erreur suppression:", e)

        await message.channel.send(f"🚀 {len(all_links)} liens traités et nettoyés")

        # 👉 suppression du message déclencheur
        try:
            await message.delete()
        except Exception as e:
            print("Erreur suppression message déclencheur:", e)

        return

    # 👉 ton ancienne logique
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    if content.lower().startswith("hello"):
        user_text = content[len("hello"):].strip()

        reply = ask_ollama(user_text)
        await message.channel.send(reply)

    await bot.process_commands(message)

bot.run(TOKEN)
