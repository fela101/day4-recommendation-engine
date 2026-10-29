"""
Day 4 - Customer Recommendation Engine
Squad Python Specialization - Data Science, AI & Analytics

Core Python only for the engine (csv, collections, math are fine). No ML libraries.
"""
from __future__ import annotations

import csv
from pathlib import Path

DATA_PATH = Path("data") / "purchases.csv"
OUTPUT_PATH = Path("output") / "recommendations.csv"


def read_purchases(path: Path = DATA_PATH) -> tuple[list[dict], list[dict]]:
    """Return (valid_rows, rejected_rows). Decide what makes a purchase row unusable."""
    raise NotImplementedError


def jaccard(a: set, b: set) -> float:
    """|A intersection B| / |A union B|. Define (and test) what happens when both are empty."""
    raise NotImplementedError


class RecommendationEngine:
    """Recommends products a customer has not bought, based on similar customers."""

    def __init__(self, purchases: list[dict], min_similarity: float = 0.0) -> None:
        # TODO: build customer -> set of products, product -> name/category,
        # and product -> purchase count (popularity) structures here, once.
        raise NotImplementedError

    def history(self, customer_id: str) -> set[str]:
        raise NotImplementedError

    def similarity(self, customer_a: str, customer_b: str) -> float:
        raise NotImplementedError

    def similar_customers(self, customer_id: str, k: int = 3) -> list[tuple[str, float]]:
        """Return the k most similar other customers as (customer_id, score), best first."""
        raise NotImplementedError

    def candidate_products(self, customer_id: str, k: int = 3) -> dict[str, dict]:
        """Products bought by similar customers but not by this one, with the evidence for each."""
        raise NotImplementedError

    def score(self, evidence: dict) -> float:
        """Your ranking rule. Combine similarity with at least one other signal."""
        raise NotImplementedError

    def recommend(self, customer_id: str, n: int = 3) -> list[dict]:
        """Return up to n ranked recommendations for one customer."""
        raise NotImplementedError

    def recommend_all(self, n: int = 3) -> list[dict]:
        raise NotImplementedError

    def export_csv(self, rows: list[dict], path: Path = OUTPUT_PATH) -> None:
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: build the engine, print recommendations for two customers, export all
    pass
