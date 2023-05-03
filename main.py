import asyncio
import concurrent

from bot.config import DISCORD_TOKEN
from bot.discord_bot import client as discord_client
from bot.telegram_bot import dp


async def main():
    while True:
        try:
            await asyncio.gather(
                discord_client.start(DISCORD_TOKEN),
                dp.start_polling()
            )

            try:
                await asyncio.Event().wait()
            except concurrent.futures.CancelledError:
                print("CancelledError occurred. The operation was cancelled.")
            finally:
                await discord_client.close()
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 10 seconds...")
            await asyncio.sleep(10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait_for(main(), timeout=None))
    except (concurrent.futures.CancelledError, asyncio.TimeoutError) as e:
        print(f"An error occurred: {e}")
    finally:
        loop.close()
