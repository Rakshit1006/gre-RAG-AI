"""Explanation prompt templates for ETS-aligned content."""

EXPLANATION_SYSTEM_PROMPT = """You will be given a selection and domain (quant/verbal/vocab/awa). Provide:
1) A short summary (1-2 sentences).
2) If verbal/RC - main idea lines and exact lines that support or contradict each answer option.
3) If quant - final numeric answer + step-by-step solution and a one-line faster method if exists.
4) If vocab - precise definition, nuance in context, and a suggested mnemonic (1-2 lines) in prude style.
5) If AWA - list key evaluation points referencing ETS rubric (thesis, evidence, organization) and give a suggested paragraph rewrite.

Return JSON: {summary, details, references:[]}. Do not hallucate external URLs (unless directly extracted from input).

Return ONLY valid JSON with no additional text."""


def create_explanation_prompt(
    selection_text: str,
    domain: str,
    depth: str = "short"
) -> str:
    """Create explanation prompt."""
    depth_instruction = {
        "short": "Keep the explanation brief and concise.",
        "detailed": "Provide a detailed explanation with reasoning.",
        "step-by-step": "Provide a complete step-by-step walkthrough."
    }.get(depth, "Keep the explanation brief and concise.")
    
    return f"""{EXPLANATION_SYSTEM_PROMPT}

DOMAIN: {domain}
DEPTH: {depth} - {depth_instruction}

TEXT TO EXPLAIN:
{selection_text}

Provide an ETS-aligned explanation and return JSON."""


AWA_GRADING_PROMPT = """You are an ETS-aligned AWA grader. Grade the essay using this rubric:
- Thesis (0-2): Clear position and understanding
- Development (0-2): Evidence, reasoning, examples
- Organization (0-1): Logical flow and structure
- Language (0-1): Grammar, vocabulary, style

Provide:
1. Overall score (0-6): Sum of rubric scores
2. Breakdown with justification for each component
3. List of specific weaknesses
4. Suggested improvements
5. A rewritten model paragraph demonstrating better execution

Return JSON: {score, rubric: {thesis, development, organization, language, justification: {thesis: "...", ...}}, weaknesses: [...], improvements: [...], suggested_draft: "..."}

Return ONLY valid JSON with no additional text."""


def create_awa_grading_prompt(essay_text: str, task_type: str) -> str:
    """Create AWA grading prompt."""
    task_description = {
        "issue": "Analyze an Issue - Present a position on an issue",
        "argument": "Analyze an Argument - Critique the logic of an argument"
    }.get(task_type, task_type)
    
    return f"""{AWA_GRADING_PROMPT}

TASK TYPE: {task_description}

ESSAY TO GRADE:
{essay_text}

Grade this essay and return JSON."""
