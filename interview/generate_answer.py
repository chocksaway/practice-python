import re
from typing import List, Dict, Callable, Any

SYSTEM_PROMPT = (
    "You are an assistant that must answer questions using ONLY the provided context. "
    "If the context is insufficient, reply: 'I don't know.' "
    "Cite the source for each fact in-line using the source id in square brackets, e.g. [roaming-policy.md::0]."
)

def build_context_message(chunks: List[Dict], max_chars: int = 8000) -> str:
    parts = []
    total = 0
    for c in chunks:
        part = f"[{c['id']}]\n{c['text']}\n"
        if total + len(part) > max_chars:
            break
        parts.append(part)
        total += len(part)
    return "\n---\n".join(parts)

# Accept several shapes: string, {"content": str}, OpenAI-like {"choices":[{"message":{"content": str}}]}
def _normalize_llm_output(resp: Any) -> str:
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        if "content" in resp:
            return resp["content"]
        if "choices" in resp:
            # OpenAI ChatCompletion shape
            try:
                return resp["choices"][0]["message"]["content"]
            except Exception:
                pass
    raise ValueError("Unrecognized LLM response shape")

"""
Build prompt from chunks + question, call llm(messages) and return {'answer', 'sources'}.
If llm is None, an attempt to call OpenAI would be made (not used in tests).
"""
def generate_answer(
    question: str,
    chunks: List[Dict],
    llm: Callable[[List[Dict]], Any] = None,
    max_chars: int = 8000,
    temperature: float = 0.0,
    max_tokens: int = 400,
) -> Dict:
    context_block = build_context_message(chunks, max_chars=max_chars)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "Context:\n" + context_block},
        {"role": "user", "content": "Question: " + question},
    ]

    if llm is None:
        # Lazy import so tests don't require openai package
        import openai  # type: ignore
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    else:
        resp = llm(messages)

    answer_text = _normalize_llm_output(resp).strip()

    # extract citations like [file.md::0]
    cites = re.findall(r"\[([^\]]+)\]", answer_text)
    # preserve order, dedupe
    seen = set()
    sources = []
    for c in cites:
        if c not in seen:
            seen.add(c)
            sources.append(c)
    return {"answer": answer_text, "sources": sources}