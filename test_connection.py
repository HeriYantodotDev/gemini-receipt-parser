import os
import sys
from dotenv import load_dotenv
from google import genai

# This is just for testing the connection

# 1. Load your .env file
load_dotenv()

if not os.environ.get("GEMINI_API_KEY"):
    print("Error: GEMINI_API_KEY not found in .env")
    sys.exit(1)

# 2. Initialize client
client = genai.Client(http_options={"timeout": 15000})

# 3. List of free, fast models ordered from least crowded to standard
MODELS_TO_TRY = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.8-flash",
]

# 4. Loop through until one responds
for model_name in MODELS_TO_TRY:
    try:
        print(f"Testing connection with {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents="Why people love money? Once sentence only response",
        )

        if response.text:
            print(f"\nSUCCESS using {model_name}!")
            print(f"Response Received: {response.text.strip()}")
            print("Environment is perfectly configured!")
            break  # Stop the loop once we succeed

    except Exception as e:  # noqa: BLE001
        print(f"Server busy or unavailable on {model_name}: {e}\nTrying next model...")