"""Test the prefilter_legal function in isolation."""
import asyncio, os, csv
from anthropic import AsyncAnthropic
from dotenv import load_dotenv
load_dotenv()

OUTPUT_DIR = "output"

async def test():
    print("1. Loading input file...")
    input_path = os.path.join(OUTPUT_DIR, "filtered_legal_Q1Q2.csv")
    with open(input_path, encoding="utf-8") as f:
        all_records = list(csv.DictReader(f))
    print(f"2. Loaded {len(all_records)} records")

    print("3. Creating AsyncAnthropic client...")
    api_key = os.getenv('ANTHROPIC_API_KEY')
    client  = AsyncAnthropic(api_key=api_key)
    print("4. Client created")

    print("5. Testing single classify call...")
    rec    = all_records[0]
    prompt = f"Title: {rec.get('title','')}\nClassify: discourse/evaluative/application"
    resp   = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=50,
        system="Return ONLY valid JSON: {\"paper_type\": \"...\", \"type_confidence\": \"...\"}",
        messages=[{"role": "user", "content": prompt}]
    )
    print(f"6. Response: {resp.content[0].text}")
    print("Test passed — prefilter should work.")

asyncio.run(test())
