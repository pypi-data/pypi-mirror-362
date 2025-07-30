import pandas as pd
import pytest
from rag_evaluation.evaluator import evaluate_response


class DummyClient:
    def __init__(self, ret):
        self.ret = ret

    # for OpenAI style
    class chat:
        class completions:
            @staticmethod
            def create(model, messages, temperature, max_tokens):
                class R:
                    choices = [
                        type("C", (), {"message": type("M", (), {"content": " 4\n"})()})
                    ]

                return R()

    # for Gemini style (if you want to test that path, stub out generate_content similarly)


def test_evaluate_response_default_weights(monkeypatch):
    # monkeypatch evaluate_openai so we don’t actually call OpenAI
    monkeypatch.setattr(
        "rag_evaluation.evaluator.evaluate_openai",
        lambda criteria, steps, query, document, response, metric_name, client, model: 5,
    )
    # supply minimal args
    df = evaluate_response(
        query="Q",
        response="R",
        document="D",
        model_type="openai",
        model_name="gpt-4",
        openai_client=DummyClient(None),
    )
    # Should be 6 rows? No—5 metrics + Overall Accuracy row
    assert isinstance(df, pd.DataFrame)
    assert "Overall Accuracy" in df.index or "Overall Accuracy" in df["Metric"].values


def test_invalid_metric_weights():
    with pytest.raises(ValueError):
        evaluate_response(
            query="Q",
            response="R",
            document="D",
            model_type="openai",
            model_name="gpt-4",
            metric_weights=[0.5, 0.5],  # wrong length/sum
        )
