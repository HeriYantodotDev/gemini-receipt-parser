# pyright: reportAttributeAccessIssue=false
# pyright: reportArgumentType=false
# pyright: ignore
# mypy: ignore-errors
# ruff: noqa
# TODO: Fix the Linting errors.

from dotenv import load_dotenv
from google import genai

# load_dotenv()
load_dotenv()

client = genai.Client()

history = [
    {
        "type": "user_input",
        "content": [{"type": "text", "text": "I have 2 dogs in my house."}],
    }
]

interaction1 = client.interactions.create(
    model="gemini-3.5-flash-lite", store=False, input=history
)
print("Response 1:", interaction1.steps[-1].content[0].text)

for step in interaction1.steps:
    history.append(step.model_dump())

history.append(
    {
        "type": "user_input",
        "content": [{"type": "text", "text": "How many paws are in my house?"}],
    }
)

interaction2 = client.interactions.create(
    model="gemini-3.5-flash-lite", store=False, input=history
)
print("Response 2:", interaction2.steps[-1].content[0].text)

print(history)
