from huggingface_hub import InferenceClient
from PIL import Image, ImageEnhance, ImageFilter
from config import HF_API_KEY

# Create Hugging Face client
client = InferenceClient(
    provider="hf-inference",
    api_key=HF_API_KEY,
)

# Supported working model
MODEL = "black-forest-labs/FLUX.1-schnell"


def generate_image_from_text(prompt):
    """
    Generate image from text prompt
    """

    print("Generating image using FLUX model...\n")

    image = client.text_to_image(
        prompt,
        model=MODEL
    )

    return image.convert("RGB")


def post_process_image(image):
    """
    Apply post-processing effects
    """

    # Brightness
    image = ImageEnhance.Brightness(image).enhance(1.2)

    # Contrast
    image = ImageEnhance.Contrast(image).enhance(1.3)

    # Slight blur
    image = image.filter(
        ImageFilter.GaussianBlur(radius=1)
    )

    return image


def main():

    print("Welcome to the Post-Processing Magic Workshop!")
    print("This program generates AI images.")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input(
            "Enter image prompt:\n"
        ).strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            print("Please enter a valid prompt.\n")
            continue

        try:

            print("\nGenerating image...")

            image = generate_image_from_text(user_input)

            print("Applying post-processing...\n")

            processed_image = post_process_image(image)

            processed_image.show()

            save_option = input(
                "\nSave image? (yes/no): "
            ).strip().lower()

            if save_option == "yes":

                file_name = input(
                    "Enter file name: "
                ).strip()

                if not file_name:
                    file_name = "generated_image"

                processed_image.save(f"{file_name}.png")

                print(f"Saved as {file_name}.png\n")

            print("-" * 80)

        except Exception as e:

            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
