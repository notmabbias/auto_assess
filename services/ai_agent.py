import os
from dotenv import load_dotenv

# load variables from .env (openAI key)
load_dotenv()

# grab key
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("found api key")
else:
    print("no key found")

