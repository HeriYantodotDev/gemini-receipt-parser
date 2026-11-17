import os
import sys
from dotenv import load_dotenv
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(http_options={"timeout": 30000})

class ReceiptData(BaseModel):
    merchant_name: str = Field(..., description="Name of the merchant")
    date: str = Field(..., description="Date of the transaction")
    total_amount: float = Field(..., description="Total amount spent")

def extract_receipt(image_path: str, model_name: str):
    print (f"Analyzing {image_path} with {model_name}")

    img = Image.open(image_path)
    response = client.models.generate_content(
        model=model_name,
        contents=["Extract the merchant name, date, and total amount.", img],
        config=types.GenerateContentConfig(
            temperature=0.0, # Zero creativity, maximum factuality
            response_mime_type="application/json",
            response_schema=ReceiptData,
        ),
    )
    print(response.text)
    return response.text

if __name__ == "__main__":
    if not os.path.exists("receipt.jpg"):
        print("Error: Please place a receipt photo named 'receipt.jpg' in the project folder.")
        sys.exit(1)
        
    try:
        # Pass the image file and the fast model that succeeded earlier
        json_result = extract_receipt("receipt.jpg", "gemini-3.5-flash-lite")
        print("\n--- Extracted Data ---")
        print(json_result)
    except Exception as e:
        print(f"Extraction failed: {e}")