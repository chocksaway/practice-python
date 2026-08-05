# Take-Home Exercise: RAG-Powered Q&A Application

## Background

Vodafone customer support and internal teams maintain a lot of knowledge in short documents — plan details, policies, FAQs. Rather than hardcoding answers, we want to explore whether an LLM can answer questions **grounded in this documentation**, citing where each answer came from.

This exercise asks you to build a small Retrieval-Augmented Generation (RAG) pipeline over a sample knowledge base of Vodafone-style documents (included in `knowledge-base/`).

## The Task

Write a program that answers a user's question using RAG. Instead of sending the question directly to an LLM, your program should first retrieve relevant context from the provided documents, then use that context to generate a grounded answer.

### Your program should:

1. **Ingest** the documents in `knowledge-base/` — load them, split them into chunks, and generate embeddings for each chunk.
2. **Store** the embeddings in a simple vector store (in-memory, FAISS, Chroma, or similar — your choice).
3. **Retrieve** the top-k most relevant chunks for a given user question.
4. **Generate** an answer by passing the retrieved context + question to an LLM.
5. **Return** the answer along with the source document(s)/chunk(s) used.

### Interface

A CLI or simple script is fine, e.g.:

```
python main.py "How much does the Roam Further World pass cost per day?"
```

### Provider choice

You may use any LLM provider or embedding model (OpenAI, Anthropic, local models via Ollama, sentence-transformers, etc.).

## Knowledge Base

The `knowledge-base/` folder contains 6 sample markdown documents:

| File | Topic |
|---|---|
| `mobile-plans.md` | Pay Monthly SIM/device plan tiers, contracts, multi-SIM discounts |
| `roaming-policy.md` | EU and rest-of-world roaming charges and rules |
| `broadband-plans.md` | Home broadband tiers, contracts, exit fees |
| `customer-support-faq.md` | Common support queries (lost phone, PAC codes, billing) |
| `network-coverage.md` | 4G/5G rollout, rural coverage, reporting outages |
| `business-plans.md` | Business mobile plans, V-Hub, IoT connectivity |

You are welcome to add your own documents to test edge cases, as long as the ones provided still work.

Note: all content in this knowledge base is fictional and written for this exercise — it does not reflect real Vodafone pricing, policy, or products.

## Suggested Test Questions

Use these to sanity-check your own pipeline before submitting. We will run similar (but not necessarily identical) questions when reviewing your submission.

**Should retrieve correctly and answer accurately:**
- "What data allowance does the Smart M plan include?"
- "How much does the Roam Further World pass cost per day?"
- "How do I request a PAC code?"
- "What's the minimum contract term for a Business Advanced plan?"
- "Does roaming cover cruise ships?"

**Should be answerable but requires connecting two facts from the same or different docs:**
- "If I'm on Smart S and want to roam in France, what do I need to do?"
- "I've had my phone on a 24-month contract for 22 months — can I upgrade early?"

**Should NOT be answered confidently (not in the knowledge base) — your program should say it doesn't know rather than guessing:**
- "What is Vodafone's current share price?"
- "Does Vodafone offer a student discount on broadband?"

## Deliverables

- We will go through your source code during the interview, so make sure it runs on the day.

## Time Expectation

This should take a couple of hours for someone comfortable with Python and basic LLM APIs. Focus on getting a clean, correct, well-reasoned pipeline working end-to-end rather than adding extra features. We're much more interested in your understanding of *why* each RAG step matters than in seeing every possible bell and whistle.

## What We're Looking For

- Does retrieval actually work (does the right document surface for a given question)?
- Is the final answer grounded in the retrieved context rather than the model's general knowledge?
- Does the program handle "no relevant answer found" gracefully instead of hallucinating?
- Did you think about practical tradeoffs (chunk size, cost, latency, caching)?

Good luck — and feel free to note any assumptions you made in your submission.
