import sys
import asyncio
import importlib
from flask import Flask
import threading
import config
from RISHUCHATBOT import ID_CHATBOT
from pyrogram import idle
from pyrogram.types import BotCommand
from config import OWNER_ID
from RISHUCHATBOT import LOGGER, RISHUCHATBOT, userbot, load_clone_owners
from RISHUCHATBOT.modules import ALL_MODULES
from RISHUCHATBOT.modules.Clone import restart_bots
from RISHUCHATBOT.modules.Id_Clone import restart_idchatbots

# Flask server for uptime ping
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

async def anony_boot():
    try:
        await RISHUCHATBOT.start()
        LOGGER.info("RISHUCHATBOT started successfully.")

        try:
            await RISHUCHATBOT.send_message(int(OWNER_ID), f"**{RISHUCHATBOT.mention} Is started ✅**")
        except Exception as ex:
            LOGGER.warning("Unable to DM OWNER_ID: start the bot manually.")

        # Import all modules BEFORE idle
        for all_module in ALL_MODULES:
            importlib.import_module("RISHUCHATBOT.modules." + all_module)
            LOGGER.info(f"Successfully imported module: {all_module}")

        # Set bot commands
        try:
            await RISHUCHATBOT.set_bot_commands(
                commands=[
                    BotCommand("start", "Start the bot"),
                    BotCommand("help", "Get the help menu"),
                    BotCommand("clone", "Make your own chatbot"),
                    BotCommand("idclone", "Make your id-chatbot"),
                    BotCommand("cloned", "Get List of all cloned bot"),
                    BotCommand("ping", "Check if the bot is alive or dead"),
                    BotCommand("lang", "Select bot reply language"),
                    BotCommand("chatlang", "Get current using lang for chat"),
                    BotCommand("resetlang", "Reset to default bot reply lang"),
                    BotCommand("id", "Get users user_id"),
                    BotCommand("stats", "Check bot stats"),
                    BotCommand("gcast", "Broadcast any message to groups/users"),
                    BotCommand("chatbot", "Enable or disable chatbot"),
                    BotCommand("status", "Check chatbot enable or disable in chat"),
                    BotCommand("shayri", "Get random shayri for love"),
                    BotCommand("ask", "Ask anything from chatgpt"),
                ]
            )
            LOGGER.info("Bot commands set successfully.")
        except Exception as ex:
            LOGGER.error(f"Failed to set bot commands: {ex}")

        # Restart clone bots
        asyncio.create_task(restart_bots())
        asyncio.create_task(restart_idchatbots())

        # Load clone owners
        await load_clone_owners()

        # Start userbot if STRING1 exists
        if config.STRING1:
            try:
                await userbot.start()
                LOGGER.info("Userbot started successfully.")
                try:
                    await RISHUCHATBOT.send_message(int(OWNER_ID), "**Id-Chatbot Also Started ✅**")
                except Exception as ex:
                    LOGGER.warning("Userbot started but couldn't message owner.")
            except Exception as ex:
                LOGGER.error(f"Error starting userbot: {ex}")

        LOGGER.info(f"@{RISHUCHATBOT.username} is up and running.")
        await idle()
        await RISHUCHATBOT.stop()
        if config.STRING1:
            await userbot.stop()

    except Exception as e:
        LOGGER.error(f"Unhandled exception in boot: {e}")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(anony_boot())