# ============================ PART 2 (PASTE INTO PART 1) ============================
# Paste this block by REPLACING the two stub functions in Part 1:
# - generate_text(...)
# - generate_exact_sentence(...)

def generate_text(prompt: str, max_new_tokens: int = 220) -> str:
    txt, err = _run_models(TEXT_MODELS, [{"role": "user", "content": prompt}], max_tokens=max_new_tokens, temperature=0.4)
    if not txt:
        raise Exception(err)
    return txt

def generate_exact_sentence(prompt: str, n_words: int, max_new_tokens: int, tries: int = 6) -> str:
    last = ""
    for _ in range(tries):
        last = generate_text(prompt, max_new_tokens=max_new_tokens)
        if len(_words(last)) >= n_words:
            return _ensure_sentence_end(_exact_n_words(last, n_words))
        prompt += f"\n\nTry again. Ensure at least {n_words} words and end with a period."
        time.sleep(0.2)
    return _ensure_sentence_end(_exact_n_words(last, min(n_words, len(_words(last)))))
