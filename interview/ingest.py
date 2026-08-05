import re
import math
from collections import Counter
from pathlib import Path

def tokenize(text):
    return [t for t in re.findall(r"\w+", text.lower()) if t]

def vectorize(tokens):
    # simple count-vector "embedding"
    return Counter(tokens)

def cosine_sim(a, b):
    common = set(a.keys()) & set(b.keys())
    num = sum(a[k] * b[k] for k in common)
    denom_a = math.sqrt(sum(v * v for v in a.values()))
    denom_b = math.sqrt(sum(v * v for v in b.values()))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return num / (denom_a * denom_b)

def chunk_text(text, max_words=200):
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks = []
    for p in paras:
        words = p.split()
        if len(words) <= max_words:
            chunks.append(p)
        else:
            for i in range(0, len(words), max_words):
                chunks.append(" ".join(words[i : i + max_words]))
    return chunks

def load_chunks(kb_dir: Path):
    md_files = sorted(kb_dir.glob("*.md"))
    chunks = []
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        for idx, c in enumerate(chunk_text(text)):
            chunks.append({"text": c, "source": f.name, "id": f"{f.name}::{idx}"})
    return chunks, md_files