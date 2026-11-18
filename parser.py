import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from pydantic import BaseModel, Field

load_dotenv()
client = genai.Client(http_options={"timeout": 30000})


class ReceiptData(BaseModel):
    merchant_name: str = Field(..., description="Name of the merchant")
    date: str = Field(..., description="Date of the transaction")
    total_amount: float = Field(..., description="Total amount spent")


def extract_receipt(image_path: str, model_name: str) -> str:
    print(f"Analyzing {image_path} with {model_name}")

    # Official SDK method to read local image bytes using a standard string path
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg",
    )
    text_part = types.Part.from_text(
        text="Extract the merchant name, date, and total amount."
    )

    # Wrap the parts in a single official types.Content object
    # Passing a single Content object to contents= completely bypasses Mypy's list invariance check
    user_content = types.Content(
        role="user",
        parts=[text_part, image_part],
    )

    response = client.models.generate_content(
        model=model_name,
        contents=user_content,
        config=types.GenerateContentConfig(
            temperature=0.0,  # Zero creativity, maximum factuality
            response_mime_type="application/json",
            response_schema=ReceiptData,
        ),
    )

    if not response.text:
        msg = "API returned an empty response."
        raise ValueError(msg)

    return response.text


if __name__ == "__main__":
    receipt_file = "receipt.jpg"
    if not os.path.exists(receipt_file):
        print(f"Error: Please place '{receipt_file}' in the project folder.")
        sys.exit(1)

    # Catch specific Google API and file errors instead of a blind 'Exception'
    try:
        json_result = extract_receipt(receipt_file, "gemini-3.5-flash-lite")
        print("\n--- Extracted Data ---")
        print(json_result)
    except (errors.APIError, OSError, ValueError) as e:
        print(f"Extraction failed: {e}")
