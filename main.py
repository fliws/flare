import asyncio
import concurrent

from .config import DISCORD_TOKEN
from .discord_bot import client as discord_client
from .telegram_bot import telegram_client


async def main():
    await discord_client.start(DISCORD_TOKEN)

    try:
        await asyncio.Event().wait()
    finally:
        await telegram_client.close()
        await discord_client.close


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait_for(main(), timeout=None))
    except (concurrent.futures.CancelledError, asyncio.TimeoutError) as e:
        print(f"An error occurred: {e}")
    finally:
        loop.close()
