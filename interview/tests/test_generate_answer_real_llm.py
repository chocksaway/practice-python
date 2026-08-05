import os
import time
import logging
from pathlib import Path

import pytest
import openai
from interview.generate_answer import generate_answer
from interview.ingest import load_chunks, tokenize, vectorize

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

@pytest.mark.real_llm
def test_generate_answer_with_real_openai():
    if os.getenv("RUN_REAL_LLM_TESTS", "0") not in ("1", "true", "True"):
        pytest.skip("Set RUN_REAL_LLM_TESTS=1 to run real-LLM tests")
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")

    repo_root = Path(__file__).resolve().parents[2]
    kb_dir = repo_root / "interview" / "knowledge-base"
    logger.info("KB dir: %s", kb_dir)

    if not kb_dir.exists():
        pytest.skip("knowledge-base directory not found: interview/knowledge-base")

    chunks, md_files = load_chunks(kb_dir)
    logger.info("Found %d markdown files; %d chunks", len(md_files), len(chunks))
    if not chunks:
        pytest.skip("No markdown files / chunks found in knowledge-base")

    chunk_vecs = [vectorize(tokenize(c["text"])) for c in chunks]

    logger.info("Generated embeddings for %d chunks", len(chunk_vecs))
    question = "How much does the Roam Further World pass cost per day?"

    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    logger.info("Running real-LLM test (model=%s). RUN_REAL_LLM_TESTS=%s", model, os.getenv("RUN_REAL_LLM_TESTS"))

    def llm_wrapper(messages):
        logger.info("Calling OpenAI with %d messages; question preview: %s", len(messages), question[:120])
        start = time.time()
        resp = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.0,
            max_tokens=200,
        )
        duration = time.time() - start
        logger.info("OpenAI call completed in %.2fs", duration)
        logger.debug("Raw OpenAI response: %s", resp)
        return resp

    out = generate_answer(question, chunks, llm=llm_wrapper, max_chars=4000, max_tokens=200)

    logger.info("Answer: %s", out.get("answer"))
    logger.info("Sources: %s", out.get("sources"))
    assert out and isinstance(out.get("answer"), str)
    assert ("£6" in out["answer"] or "6 per day" in out["answer"] or "6" in out["answer"])
    assert "roaming-policy.md::0" in out.get("sources", []), f"Sources returned: {out.get('sources')}"