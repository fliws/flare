import asyncio
import concurrent

from bot.config import DISCORD_TOKEN
from bot.discord_bot import client as discord_client
from bot.telegram_bot import telegram_client

async def main():
    await discord_client.start(DISCORD_TOKEN)

    try:
        await asyncio.Event().wait()
    except concurrent.futures.CancelledError:
        print("CancelledError occurred. The operation was cancelled.")
    finally:
        await telegram_client.close()
        await discord_client.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait_for(main(), timeout=None))
    except (concurrent.futures.CancelledError, asyncio.TimeoutError) as e:
        print(f"An error occurred: {e}")
    finally:
        loop.close()
