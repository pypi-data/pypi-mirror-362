import pytest
from rag_evaluation.utils import (
    normalize_score,
    calculate_weighted_accuracy,
    generate_report,
)
import pandas as pd


def test_normalize_score():
    assert normalize_score(3, max_score=5) == pytest.approx(0.6)
    assert normalize_score(5, max_score=5) == 1.0


def test_calculate_weighted_accuracy():
    scores = [1.0, 0.5, 0.0]
    weights = [0.2, 0.3, 0.5]
    # weighted sum = 1*0.2 + 0.5*0.3 + 0*0.5 = 0.2 + 0.15 = 0.35
    assert calculate_weighted_accuracy(scores, weights) == pytest.approx(0.35)


def test_generate_report():
    scores = [5, 3]
    weights = [0.5, 0.5]
    names = ["A", "B"]
    df = generate_report(scores, weights, names, max_score=5)
    # Should have 3 rows (A, B, Overall Accuracy)
    assert list(df["Metric"]) == ["A", "B", "Overall Accuracy"]
    # Normalized for A=1.0, B=0.6
    assert df.loc[0, "Score (%)"] == 100
    assert df.loc[1, "Score (%)"] == 60
    # Overall = (1.0*0.5 + 0.6*0.5) = 0.8 → 80%
    assert df.loc[2, "Score (%)"] == pytest.approx(80)
