import re
from interview.generate_answer import generate_answer

def test_generate_answer_with_mock_llm():
    # sample chunks
    chunks = [
        {"id": "roaming-policy.md::0", "source": "roaming-policy.md", "text": "Roam Further World pass costs £6 per day."},
        {"id": "mobile-plans.md::0", "source": "mobile-plans.md", "text": "Smart M includes 20GB data allowance."},
    ]

    question = "How much does the Roam Further World pass cost per day?"

    def mock_llm(messages):
        # assert context and question are present
        joined = "\n".join(m["content"] for m in messages if m.get("content"))
        assert "Roam Further World pass costs £6 per day." in joined
        assert question in joined
        # return a plausible assistant response including a citation
        return {"content": "The Roam Further World pass costs £6 per day. [roaming-policy.md::0]"}

    out = generate_answer(question, chunks, llm=mock_llm)
    assert "£6" in out["answer"]
    assert out["sources"] == ["roaming-policy.md::0"]

def test_generate_answer_no_citation():
    chunks = [
        {"id": "mobile-plans.md::0", "source": "mobile-plans.md", "text": "Smart M includes 20GB data allowance."},
    ]
    question = "What is the data allowance of Smart M?"
    def mock_llm(messages):
        return "Smart M includes 20GB data allowance."  # no citation
    out = generate_answer(question, chunks, llm=mock_llm)
    assert "20GB" in out["answer"]
    assert out["sources"] == []