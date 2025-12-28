import requests

from config import HF_API_KEY

 

# Model endpoint on Hugging Face

MODEL_ID = "nlpconnect/vit-gpt2-image-captioning"

API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

 

# Prepare headers with your API key

headers = {

    "Authorization": f"Bearer {HF_API_KEY}"

}

 

def caption_single_image():

    """

    Loads the local image file "test.jpg" and sends it to the

    Hugging Face Inference API for captioning.

    """

    image_source = "test.jpg"  # Hardcoded filename

   

    # 1. Load image bytes

    try:

        with open(image_source, "rb") as f:

            image_bytes = f.read()

    except Exception as e:

        print(f"Could not load image from {image_source}.\nError: {e}")

        return

 

    # 2. Send request to the Hugging Face Inference API

    response = requests.post(API_URL, headers=headers, data=image_bytes)

    result = response.json()

 

    # 3. Check for errors

    if isinstance(result, dict) and "error" in result:

        print(f"[Error] {result['error']}")

        return

 

    # 4. Extract caption

    caption = result[0].get("generated_text", "No caption found.")

    print("Image:", image_source)

    print("Caption:", caption)

 

def main():

    # Caption the hardcoded file

    caption_single_image()

 

if __name__ == "__main__":

    main()

 