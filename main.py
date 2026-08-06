#!/usr/bin/env python3
"""Simple CLI to ask a question against interview/knowledge-base using OpenAI.

Usage:
  dotenv run -- python main.py "How much does the Roam Further World pass cost per day?"

It follows the flow from tests/test_generate_answer_real_llm.py: load chunks, call OpenAI, print answer and sources.
"""
import os
import time
import logging
import argparse
from pathlib import Path

import openai
from interview.generate_answer import generate_answer
from interview.ingest import load_chunks, tokenize, vectorize

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    p = argparse.ArgumentParser(description="Ask a question against the interview knowledge-base using OpenAI")
    p.add_argument("question", nargs="+", help="Question to ask (wrap in quotes)")
    args = p.parse_args()

    question = " ".join(args.question).strip()

    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY not set in environment")
        return 2

    repo_root = Path(__file__).resolve().parent
    kb_dir = repo_root / "interview" / "knowledge-base"
    if not kb_dir.exists():
        logger.error("knowledge-base directory not found: %s", kb_dir)
        return 2

    chunks, md_files = load_chunks(kb_dir)
    logger.info("Found %d markdown files; %d chunks", len(md_files), len(chunks))
    if not chunks:
        logger.error("No markdown files / chunks found in knowledge-base")
        return 2

    # Precompute simple "embeddings" (count vectors) - useful if later retrieval is added
    chunk_vecs = [vectorize(tokenize(c["text"])) for c in chunks]
    logger.info("Generated embeddings for %d chunks", len(chunk_vecs))

    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    logger.info("Running LLM (model=%s)", model)

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

    print("\nANSWER:\n")
    print(out.get("answer"))
    print("\nSOURCES:\n")
    for s in out.get("sources", []):
        print(" - ", s)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
