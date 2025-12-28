from config import HF_API_KEY

import requests

from PIL import Image

import io

import os

from colorama import init, Fore, Style

import json

 

# Initialize Colorama for colorful output

init(autoreset=True)

 

# -----------------------------------------------------------------------------

# Utility function to send API requests

# -----------------------------------------------------------------------------

def query_hf_api(api_url, payload=None, files=None, method="post"):

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    try:

        if method.lower() == "post":

            # When files provided, send them along with the payload.

            response = requests.post(api_url, headers=headers, json=payload, files=files)

        else:

            response = requests.get(api_url, headers=headers, params=payload)

        if response.status_code != 200:

            raise Exception(f"Status {response.status_code}: {response.text}")

        return response.content

    except Exception as e:

        print(f"{Fore.RED}❌ Error while calling API: {e}")

        raise

 

# -----------------------------------------------------------------------------

# Task: Get a basic caption from an image using an image captioning model.

# -----------------------------------------------------------------------------

def get_basic_caption(image, model="nlpconnect/vit-gpt2-image-captioning"):

    print(f"{Fore.YELLOW}???? Generating basic caption using vit-gpt2-image-captioning ...")

    api_url = f"https://api-inference.huggingface.co/models/{model}"

    buffered = io.BytesIO()

    # Save as JPEG (this model works well with JPEG images)

    image.save(buffered, format="JPEG")

    buffered.seek(0)

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    response = requests.post(api_url, headers=headers, data=buffered.read())

    result = response.json()

    if isinstance(result, dict) and "error" in result:

        return f"[Error] {result['error']}"

    # Expecting result to be a list of dicts with 'generated_text'

    caption = result[0].get("generated_text", "No caption generated.")

    return caption

 

# -----------------------------------------------------------------------------

# Task: Generate text using a text generation model (e.g. GPT-2)

# -----------------------------------------------------------------------------

def generate_text(prompt, model="gpt2", max_new_tokens=60):

    print(f"{Fore.CYAN}???? Generating text with prompt: {prompt}")

    api_url = f"https://api-inference.huggingface.co/models/{model}"

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens}}

    text_bytes = query_hf_api(api_url, payload=payload)

    try:

        result = json.loads(text_bytes.decode("utf-8"))

    except Exception as e:

        raise Exception("Failed to decode text generation response.")

    if isinstance(result, dict) and "error" in result:

        raise Exception(result["error"])

    generated = result[0].get("generated_text", "")

    return generated

 

# -----------------------------------------------------------------------------

# Helper: Truncate text to a specific word count.

# -----------------------------------------------------------------------------

def truncate_text(text, word_limit):

    words = text.strip().split()

    return " ".join(words[:word_limit])

 

# -----------------------------------------------------------------------------

# Interactive menu for image-to-text output

# -----------------------------------------------------------------------------

def print_menu():

    print(f"""{Style.BRIGHT}

{Fore.GREEN}================ Image-to-Text Conversion =================

Select output type:

1. Caption (5 words)

2. Description (30 words)

3. Summary (50 words)

4. Exit

===============================================================

""")

 

def main():

    image_path = input(f"{Fore.BLUE}Enter the path of the image for text generation (e.g., test.jpg): {Style.RESET_ALL}")

    if not os.path.exists(image_path):

        print(f"{Fore.RED}❌ The file '{image_path}' does not exist.")

        return

    try:

        image = Image.open(image_path)

    except Exception as e:

        print(f"{Fore.RED}❌ Failed to open image: {e}")

        return

 

    # Get a basic caption from the image

    basic_caption = get_basic_caption(image)

    print(f"{Fore.YELLOW}???? Basic caption: {Style.BRIGHT}{basic_caption}\n")

 

    while True:

        print_menu()

        choice = input(f"{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}")

        if choice == "1":

            # Caption: take first 5 words from basic caption

            caption = truncate_text(basic_caption, 5)

            print(f"{Fore.GREEN}✅ Caption (5 words): {Style.BRIGHT}{caption}\n")

        elif choice == "2":

            # Description: expand basic caption to a 30-word description using GPT-2.

            prompt_text = f"Expand the following caption into a detailed description in exactly 30 words: {basic_caption}"

            try:

                generated = generate_text(prompt_text, max_new_tokens=40)

                description = truncate_text(generated, 30)

                print(f"{Fore.GREEN}✅ Description (30 words): {Style.BRIGHT}{description}\n")

            except Exception as e:

                print(f"{Fore.RED}❌ Failed to generate description: {e}")

        elif choice == "3":

            # Summary: expand basic caption to a summary in 50 words.

            prompt_text = f"Summarize the content of the image described by this caption into a summary of exactly 50 words: {basic_caption}"

            try:

                generated = generate_text(prompt_text, max_new_tokens=60)

                summary = truncate_text(generated, 50)

                print(f"{Fore.GREEN}✅ Summary (50 words): {Style.BRIGHT}{summary}\n")

            except Exception as e:

                print(f"{Fore.RED}❌ Failed to generate summary: {e}")

        elif choice == "4":

            print(f"{Fore.GREEN}???? Goodbye!")

            break

        else:

            print(f"{Fore.RED}❌ Invalid choice. Please enter a number between 1 and 4.")

 

if __name__ == "__main__":

    main()