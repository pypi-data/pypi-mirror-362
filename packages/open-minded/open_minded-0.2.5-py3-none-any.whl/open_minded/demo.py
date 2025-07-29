import asyncio
import random

from open_minded.llm_provider_aggregator import fetch_llm_completion_and_stream

random.seed(2)


async def _fetch_completion_for_demo():
    async with fetch_llm_completion_and_stream(
        [{"role": "user", "content": "Type 100 random characters"}]
    ) as completion:
        print(f"\nStreaming from {completion.provider.name}...\n")

        async for chunk in completion.result:
            print(chunk, end="")

        print("\n")


asyncio.run(_fetch_completion_for_demo())
