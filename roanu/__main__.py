import asyncio
from roanu import roanuedhuru
from better_profanity import profanity


async def main():
    profanity.add_censor_words(['ngbl', 'nagoobalha', 'balha'])

    await roanuedhuru.start()
    await roanuedhuru.idle()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
