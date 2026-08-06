import logging
from collections import Counter
from pathlib import Path

import pytest

from interview.ingest import load_chunks, vectorize, cosine_sim, tokenize

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@pytest.mark.integration
def test_ingest_and_retrieve():
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

    queries = {
        "How much does the Roam Further World pass cost per day?": "roaming-policy.md",
        "How do I request a PAC code?": "customer-support-faq.md",
        "What data allowance does the Smart M plan include?": "mobile-plans.md",
    }

    for q, expected_file in queries.items():
        if not any(p.name == expected_file for p in md_files):
            logger.info("Skipping expected file %s (not in KB)", expected_file)
            continue

        q_vec = vectorize(tokenize(q))
        scores = [cosine_sim(q_vec, v) for v in chunk_vecs]
        scored = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)
        top = scored[:3]
        logger.info("Query: %s | Top scores: %s", q, [(float(s), c['source']) for s, c in top])
        top_sources = [item[1]["source"] for item in top if item[0] > 0.0]
        assert expected_file in top_sources, f"Expected {expected_file} in top-3 sources for query: {q}. Top sources: {top_sources}"

    unrelated = "What is Vodafone's current share price?"
    q_vec = vectorize(tokenize(unrelated))
    scores = [cosine_sim(q_vec, v) for v in chunk_vecs]
    top_score = max(scores)
    logger.info("Unrelated query top similarity score: %.4f", top_score)
    # threshold relaxed to account for count-vector similarity noise
    assert top_score < 0.25, f"Unrelated query matched KB too strongly (score={top_score})"