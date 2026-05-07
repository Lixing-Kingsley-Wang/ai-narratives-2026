import asyncio, os
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
load_dotenv()

async def test():
    key = os.getenv('ANTHROPIC_API_KEY')
    print(f"Key loaded: {bool(key)}")
    print(f"Key prefix: {key[:10] if key else 'NONE'}")
    
    client = AsyncAnthropic(api_key=key)
    print("Client created. Making API call...")
    
    r = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=20,
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print(f"Response: {r.content[0].text}")
    print("Async API works correctly.")

asyncio.run(test())
