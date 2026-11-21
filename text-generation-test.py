# Text Generation test from the API
# https://aistudio.google.com/u/3/docs/text-generation?codelanguage=python
# The second file is in stateless.py,
# TODO: Linting errors.

from dotenv import load_dotenv
from google import genai

# load_dotenv()
load_dotenv()

client = genai.Client()

uploaded_file = client.files.upload(file="images/image1.png")

input = [
    {
        "type": "text",
        "text": "Explain the image!",
    },
    {
        "type": "image",
        "uri": uploaded_file.uri,
        "mime_type": uploaded_file.mime_type,
    },
]
system_instruction1 = (
    "You are an alien, you are name is Zorblax, "
    "you are very smart and you are very funny. "
    "You are a comedian and you like to make jokes."
    "You are also a scientist "
    "and you like to explain things in a simple way."
)

system_instruction2 = (
    "You are the best communicator in the world."
    "You are going to explain this to 5 years old."
    "You are going to use a very simple language"
    "Even non English speakers will understand you."
    "You are going to use a lot of examples and metaphors."
)


interaction1 = client.interactions.create(
    model="gemini-3.5-flash-lite",
    generation_config={
        "thinking_level": "medium",  # thinking level
        "max_output_tokens": 1000,  # Set maximum output tokens.
    },
    system_instruction=system_instruction2,  # guide the behavior of Gemini models
    input=input,
)

if not hasattr(interaction1, "output_text"):
    print("error on interaction1")
    raise RuntimeError("Expected a completed interaction")

print("Interaction 1")
print("-----------")

print(interaction1.output_text or "")

interaction2 = client.interactions.create(
    model="gemini-3.5-flash-lite",
    generation_config={
        "thinking_level": "medium",  # thinking level
        "max_output_tokens": 1000,  # Set maximum output tokens.
    },
    input=(
        "Well, I have no idea what you are talking about. "
        "Can you explain it in normal language, like for an adult?"
    ),
    previous_interaction_id=interaction1.id,  # type: ignore
)

if not hasattr(interaction2, "output_text"):
    print("error on interaction2")
    raise RuntimeError("Expected a completed interaction")

print("Interaction 2")
print("-----------")
print(interaction2.output_text or "")

print("Interaction 2 End ------")
print("-----------")

stream = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input=(
        "So is this organ important for the human body?,"
        "Can you explain it in a simple way?"
    ),
    previous_interaction_id=interaction2.id,  # type: ignore
    stream=True,
)

print("Interaction Streaming ")
print("-----------")

for event in stream:
    if event.event_type == "step.delta":  # type: ignore[union-attr]  # noqa: SIM102
        if event.delta.type == "text":  # type: ignore[union-attr]
            print(event.delta.text, end="")  # type: ignore[union-attr]
