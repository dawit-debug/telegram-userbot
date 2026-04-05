from telethon import TelegramClient, events
import asyncio

api_id = 21151795
api_hash = "bf7b32111af284f78b1459fcf249489b"

client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    # Ignore your own messages
    if event.out:
        return

    text_lower = event.raw_text.lower()
    original_text = event.raw_text

    # ✅ Trigger only for airdrop-style messages with #
    if "created an airdrop" in text_lower and "#" in original_text:

        # 🔍 Extract from #
        start = original_text.index("#")
        reply_text = original_text[start:]

        # ✂️ Remove "to grab it"
        if "to grab it" in reply_text.lower():
            end = reply_text.lower().index("to grab it")
            reply_text = reply_text[:end].strip()

        reply_text = reply_text.strip()

        # ❌ Avoid empty or just "#"
        if reply_text and reply_text != "#":
            await asyncio.sleep(0)
            # 📩 Reply in same chat (group or private)
            await event.reply(reply_text)

    # 🔹 CASE 2: No # but says "send grab" - Corrected indentation
    elif "send grab" in text_lower:
        await asyncio.sleep(0)
        await event.reply("grab")

async def start_and_run_bot():
    await client.start()
    print("✅ Userbot running in groups + private...")
    await client.run_until_disconnected()

async def main_colab_runner():
    # Start the bot as a background task
    bot_task = asyncio.create_task(start_and_run_bot())

    print("Bot started in background. Keeping Colab cell alive...")

    try:
        # Keep the Colab cell alive by periodically yielding control.
        # This aims to prevent Colab from cancelling the cell due to perceived inactivity.
        while True:
            await asyncio.sleep(60 * 5) # Sleep for 5 minutes
            if bot_task.done():
                print("Bot task finished or cancelled.")
                break
    except asyncio.CancelledError:
        print("Colab cell execution cancelled. Attempting to stop bot task.")
        bot_task.cancel() # Request bot_task to cancel
        await asyncio.gather(bot_task, return_exceptions=True) # Wait for it to finish cancelling
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        bot_task.cancel()
        await asyncio.gather(bot_task, return_exceptions=True)
    finally:
        if not bot_task.done():
            print("Ensuring bot task is cancelled on exit.")
            bot_task.cancel()
            await asyncio.gather(bot_task, return_exceptions=True)
        print("Colab cell runner finished.")

import asyncio
if __name__=="__main__":
    asyncio.run(main_colab_runner())
