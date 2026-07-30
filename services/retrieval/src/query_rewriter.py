import os

import requests

QUERY_REWRITER_URL = os.environ.get("QUERY_REWRITER_URL", "http://query-rewriter:11434")
QUERY_REWRITER_MODEL = "qwen3:1.7b-q8_0"

QUERY_REWRITER_PROMPT = """You are a query rewriting assistant for a financial document search system. \
Your job is to convert conversational user questions into concise, keyword-dense search queries \
optimized for both semantic vector search and BM25 keyword search.

Rules:
- Strip greetings, filler words, and conversational phrasing.
- Resolve pronouns and vague references (e.g. "that", "it", "the previous one") using the \
conversation history provided. If there is no history, resolve as best as possible from context alone.
- Preserve all financial terms, entities, dates, and numbers exactly as given — do not paraphrase \
domain-specific terminology (e.g. "EBITDA", "operating margin", "Q3 2024").
- If the query contains two or more distinct search intents, split them into separate queries.
- If the query is already a clean, focused search query, return it unchanged.
- Output ONLY valid JSON in this exact format, with no explanation, no markdown, no preamble:

{"queries": ["<query 1>", "<query 2>"]}

If there is only one intent, return a single-element list.
"""


def rewrite_query(query: str, history: list[dict] | None = None) -> str:
    messages = [{"role": "system", "content": QUERY_REWRITER_PROMPT}]
    if history:
        messages.extend(history)  # e.g. [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    messages.append({"role": "user", "content": f"Current query: {query}"})

    response = requests.post(
        f"{QUERY_REWRITER_URL}/api/chat",
        json={
            "model": QUERY_REWRITER_MODEL,
            "messages": messages,
            "stream": False,
        },
    )
    response.raise_for_status()
    return response.json()["message"]["content"].strip()
