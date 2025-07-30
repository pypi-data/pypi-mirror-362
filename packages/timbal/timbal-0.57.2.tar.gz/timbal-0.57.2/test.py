import os

from timbal import Agent
from timbal.core.shared import RemoteConfig

# For testing purposes
os.environ["TIMBAL_API_HOST"] = "api.timbal.ai"


async def main():
    remote_config = RemoteConfig(
        org_id="1",
        app_id="49",
    )
    agent = Agent(remote_config=remote_config)

    # # You can run this in as a stream
    # async for event in agent.run(prompt="Hello"):
    #     print(event)

    # Or you can run this as a whole and get the final output event
    res = await agent.complete(prompt="Hello")
    print(res)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())