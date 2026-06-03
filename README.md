# discord-ollama

A lean Discord bot powered by Ollama for automated link curation and action-oriented AI assistance.

## 🚀 Features

- **Meta-Lead AI**: A concise assistant designed to cut through the noise, prioritize ideas, and suggest single, executable actions. No fluff, just direction.
- **Automated Link Harvesting**: Triggered by the keyword `parti`, the bot scans the last 100 messages of the current channel, extracts all URLs (using a hybrid Regex + LLM approach), aggregates them into a dedicated links channel, and cleans up the source chat by deleting the original messages.
- **Local-First AI**: Runs entirely via Ollama, ensuring privacy, zero API costs, and full control over the model.

## 🧠 Why I built this

I built this to reduce the cognitive friction of managing "idea-dense" Discord channels. In high-velocity brainstorms, valuable resources often get buried under a mountain of conversation. Instead of manually scrolling through days of chat to recover a link, I wanted a one-word trigger to "vacuum" the noise and distill it into a structured list.

Integrating Ollama allows me to have a "Meta-Lead" in the room—an entity that doesn't just chat, but pushes for clarity and action. This reflects my preference for lean, high-leverage workflows where the goal is to move from "idea" to "execution" as quickly as possible.

## 🛠️ Setup

### Prerequisites
- [Ollama](https://ollama.ai/) installed and running.
- The `gpt-oss:20b-cloud` model pulled.

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/codafine-dev/discord-ollama.git
   cd discord-ollama
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   GOOD_MORNING_SALLON_ID=channel_id_for_ai_chat
   LINKS_CHANNEL_ID=channel_id_for_link_storage
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## 📖 Usage

- **AI Assistance**: Type `hello <your question>` in the designated AI channel to get a concise, action-oriented response.
- **Link Cleanup**: Type any message containing the word `parti` to trigger the link harvester and clean up the channel history.
