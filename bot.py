from telethon import TelegramClient, events
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

api_id = 21151795
api_hash = "bf7b32111af284f78b1459fcf249489b"

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.out:
        return

    text_lower = event.raw_text.lower()
    original_text = event.raw_text

    if "created an airdrop" in text_lower:

        if "#" in original_text:
            start = original_text.index("#")
            reply_text = original_text[start:]

            if "to grab it" in reply_text.lower():
                end = reply_text.lower().index("to grab it")
                reply_text = reply_text[:end].strip()

            if reply_text and reply_text != "#":
                await asyncio.sleep(0.0001)
                await event.reply(reply_text)

        elif "send grab" in text_lower:
            await asyncio.sleep(0.0001)
            await event.reply("grab")

# 🔥 Fake web server to keep Render happy
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():
    port = 10000
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# Run web server in separate thread
threading.Thread(target=run_web).start()

# Start Telegram bot
client.start()
print("✅ Userbot running...")
client.run_until_disconnected()
