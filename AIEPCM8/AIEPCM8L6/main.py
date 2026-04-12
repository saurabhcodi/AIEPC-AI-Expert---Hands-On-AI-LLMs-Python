# ---- Part 2: paste this function into Part 1 (replace placeholder) ----
def run_safe_ai_image_generator():
    FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"

    # fallback model if needed: "black-forest-labs/FLUX.1-schnell"
    IMG_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
    img_client = InferenceClient(provider="hf-inference", api_key=config.HF_API_KEY)

    st.title("🖼️ Safe AI Image Generator")

    def is_prompt_safe(prompt: str):
        try:
            response = requests.post(
                FILTER_API_URL,
                json={"text": prompt},
                timeout=15
            )

            if response.status_code != 200:
                return False, f"Filter API failed with status {response.status_code}: {response.text}"

            data = response.json()

            if data.get("ok") is True:
                return True, None
            return False, data.get("reason", "⚠️ Unsafe prompt.")

        except Exception as e:
            return False, f"Filter API error: {e}"

    def generate_image(prompt: str):
        safe, err = is_prompt_safe(prompt)
        if not safe:
            return None, err

        try:
            image = img_client.text_to_image(prompt=prompt, model=IMG_MODEL)
            return image, None
        except Exception as e:
            return None, f"Error during image generation: {e}"

    with st.form("img_form"):
        p = st.text_area("Image description:", height=120)
        ok = st.form_submit_button("Generate Image")

    if ok:
        if not p.strip():
            st.warning("⚠️ Enter a description.")
        else:
            with st.spinner("Generating image..."):
                im, err = generate_image(p.strip())

            if err:
                st.error(err)
            else:
                st.image(im, use_container_width=True)
                st.session_state.generated_image = im

    im = st.session_state.get("generated_image")
    if im:
        buf = BytesIO()
        im.save(buf, format="PNG")
        st.download_button(
            "📥 Download",
            buf.getvalue(),
            "ai_generated_image.png",
            "image/png"
        )