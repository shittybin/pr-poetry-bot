import os
import time
from openai import OpenAI
from openai.types.chat import ChatCompletion

# Initialize client with your API key (set as env var)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Retry logic: exponential backoff in case of rate limits
def generate_poem():
    for attempt in range(5):  # max 5 retries
        try:
            response: ChatCompletion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative poet."},
                    {"role": "user", "content": "Write a short poem about GitHub pull requests."}
                ],
                temperature=0.7
            )
            print("🎉 Poem Generated:\n")
            print(response.choices[0].message.content)
            return
        except Exception as e:
            if "rate_limit" in str(e).lower() or "quota" in str(e).lower():
                wait = 2 ** attempt
                print(f"⏳ Rate limit hit or quota error: retrying in {wait} seconds...")
                time.sleep(wait)
            else:
                print(f"❌ Unexpected error: {e}")
                break

if __name__ == "__main__":
    generate_poem()
