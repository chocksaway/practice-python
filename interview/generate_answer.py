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

def _normalize_llm_output(resp: Any) -> str:
    """
    Accept several shapes and return the text content:
    - plain string
    - dict-like: {"content": str}
    - OpenAI-like dict: {"choices": [{"message": {"content": str}}]}
    - OpenAI objects: objects with .to_dict() or .choices attributes
    """
    if isinstance(resp, str):
        return resp

    # If the object can be converted to a dict (OpenAI objects often can), use that
    try:
        to_dict = getattr(resp, "to_dict", None)
        if callable(to_dict):
            d = resp.to_dict()
        else:
            d = None
    except Exception:
        d = None

    if isinstance(d, dict):
        resp = d

    if isinstance(resp, dict):
        if "content" in resp:
            return resp["content"]
        if "choices" in resp and resp["choices"]:
            try:
                return resp["choices"][0]["message"]["content"]
            except Exception:
                # try alternative keys
                try:
                    return resp["choices"][0].get("text")
                except Exception:
                    pass

    # Fallback: object with .choices attribute
    choices = getattr(resp, "choices", None)
    if choices:
        try:
            first = choices[0]
            # if first is dict-like
            if isinstance(first, dict):
                msg = first.get("message") or {}
                if isinstance(msg, dict) and "content" in msg:
                    return msg["content"]
                if "text" in first:
                    return first.get("text")
            # if first is object-like
            msg = getattr(first, "message", None)
            if msg is not None:
                if isinstance(msg, dict) and "content" in msg:
                    return msg["content"]
                content = getattr(msg, "content", None)
                if content:
                    return content
                # msg might support .get
                try:
                    g = msg.get("content")
                    if g:
                        return g
                except Exception:
                    pass
            # last resort: try first.text
            text_attr = getattr(first, "text", None)
            if text_attr:
                return text_attr
        except Exception:
            pass

    raise ValueError("Unrecognized LLM response shape")

def generate_answer(
    question: str,
    chunks: List[Dict],
    llm: Callable[[List[Dict]], Any] = None,
    max_chars: int = 8000,
    temperature: float = 0.0,
    max_tokens: int = 400,
) -> Dict:
    """
    Build prompt from chunks + question, call llm(messages) and return {'answer', 'sources'}.
    If llm is None, an attempt to call OpenAI would be made (not used in tests).
    """
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