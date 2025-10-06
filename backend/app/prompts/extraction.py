"""Question extraction prompt templates."""

QUESTION_EXTRACTION_PROMPT = """You are a question extractor. Input is a blob of text which may contain one or more GRE-style questions. Identify and extract every question with choices (if present), answer (if present), and explanation (if present). For ambiguous parts, return 'uncertain' fields. Output JSON array of objects: {question_text, choices (array|null), answer|null, explanation|null, detected_type: "text_completion|sentence_equivalence|rc|quant|unknown", confidence:0.0-1.0}. Keep outputs concise.

Return ONLY valid JSON array with no additional text."""


def create_extraction_prompt(text: str) -> str:
    """Create question extraction prompt."""
    return f"""{QUESTION_EXTRACTION_PROMPT}

TEXT TO ANALYZE:
{text}

Extract all questions and return as JSON array."""


CLIP_CLASSIFIER_PROMPT = """You are a content classifier for GRE study materials. Given a text selection, determine if it is:
1. A vocabulary word (single word or phrase with definition)
2. A practice question (with or without answer choices)
3. A concept/explanation

Return JSON with: {{"type": "word|question|concept", "confidence": 0.0-1.0, "reason": "brief explanation"}}

Return ONLY valid JSON with no additional text."""


def create_clip_classifier_prompt(text: str, hint: str = "auto") -> str:
    """Create clip classification prompt."""
    hint_text = f"\nUSER HINT: The content is likely related to {hint}." if hint != "auto" else ""
    
    return f"""{CLIP_CLASSIFIER_PROMPT}{hint_text}

TEXT TO CLASSIFY:
{text}

Classify this content and return JSON."""
