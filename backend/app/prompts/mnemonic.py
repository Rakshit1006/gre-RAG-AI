"""Mnemonic generation prompt templates."""

MNEMONIC_SYSTEM_PROMPT = """You are a GRE mnemonic generator. ALWAYS return valid JSON only (no extra commentary). Output must include the fields in this order exactly:
word, pos, gre_definition, pithy_definition, base_word, associations (array of 5 strings), examples (array of 3 strings), easy_synonyms (array of 3 strings), gre_synonyms (array of 3 strings), story (single string).

Tone: playful, sound-based, zany, memorable. Keep examples short. Use no more than 40 words in the story. If unsure about POS, return "unknown". Do not include html.

Return ONLY valid JSON with no additional text or formatting."""


def create_mnemonic_prompt(word: str, pos: str = None, style: str = "prude") -> str:
    """Create mnemonic generation prompt."""
    user_input = {
        "word": word,
        "pos": pos or "unknown",
        "style": style
    }
    
    return f"""{MNEMONIC_SYSTEM_PROMPT}

USER: {user_input}

Generate a mnemonic for the word "{word}" following the exact JSON schema above."""
