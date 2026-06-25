"""Evaluate multiple-choice predictions on StoryAD-QA CSVs."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd


CHOICES = {"A", "B", "C", "D", "E"}


def normalize_choice(value) -> str:
    text = "" if value is None else str(value).strip().upper()
    if text.startswith("OPTION_"):
        text = text.replace("OPTION_", "", 1)
    if text.startswith("OPTION "):
        text = text.replace("OPTION ", "", 1)
    return text[:1] if text[:1] in CHOICES else text


def row_key(row, idx: int, mode: str) -> Tuple[str, str]:
    file_value = str(row.get("file", "")).strip()
    row_index = str(row.get("row_index", idx)).strip()
    if mode == "row_index":
        return ("", row_index)
    if mode == "file_row_index":
        return (file_value, row_index)
    return (file_value, "")


def infer_key_mode(predictions: pd.DataFrame) -> str:
    has_file = "file" in predictions.columns
    has_row = "row_index" in predictions.columns
    if has_file and has_row:
        return "file_row_index"
    if has_row:
        return "row_index"
    if has_file:
        return "file"
    raise ValueError("Predictions must include file and/or row_index.")


def load_predictions(path: Path) -> Tuple[Dict[Tuple[str, str], str], str]:
    df = pd.read_csv(path).fillna("")
    if "prediction" not in df.columns:
        raise ValueError("Predictions CSV must contain a prediction column.")
    mode = infer_key_mode(df)
    predictions: Dict[Tuple[str, str], str] = {}
    for idx, row in df.iterrows():
        predictions[row_key(row, idx, mode)] = normalize_choice(row.get("prediction"))
    return predictions, mode


def evaluate(answers_path: Path, predictions_path: Path) -> dict:
    answers = pd.read_csv(answers_path).fillna("")
    predictions, mode = load_predictions(predictions_path)

    total = len(answers)
    evaluated = 0
    correct = 0
    missing = 0
    invalid = 0
    by_answer = defaultdict(lambda: Counter(total=0, evaluated=0, correct=0))

    for idx, row in answers.iterrows():
        answer = normalize_choice(row.get("correct_answer"))
        key = row_key(row, idx, mode)
        pred = predictions.get(key, "")
        by_answer[answer]["total"] += 1
        if not pred:
            missing += 1
            continue
        if pred not in CHOICES:
            invalid += 1
            continue
        evaluated += 1
        by_answer[answer]["evaluated"] += 1
        if pred == answer:
            correct += 1
            by_answer[answer]["correct"] += 1

    per_answer = {}
    for answer, counts in sorted(by_answer.items()):
        denom = counts["evaluated"]
        per_answer[answer] = {
            "total": counts["total"],
            "evaluated": counts["evaluated"],
            "correct": counts["correct"],
            "accuracy": counts["correct"] / denom if denom else None,
        }

    return {
        "answers": str(answers_path),
        "predictions": str(predictions_path),
        "key_mode": mode,
        "total": total,
        "evaluated": evaluated,
        "missing": missing,
        "invalid": invalid,
        "correct": correct,
        "accuracy": correct / evaluated if evaluated else None,
        "per_answer": per_answer,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate StoryAD-QA multiple-choice predictions.")
    parser.add_argument("--answers", type=Path, help="StoryAD-QA CSV containing the answer key.")
    parser.add_argument("--gold", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--predictions", type=Path, required=True, help="Prediction CSV.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()
    if args.answers is None:
        args.answers = args.gold
    if args.answers is None:
        parser.error("--answers is required")
    return args


def main() -> None:
    args = parse_args()
    result = evaluate(args.answers, args.predictions)
    if args.json:
        print(json.dumps(result, indent=2))
        return
    print(f"Answers: {result['answers']}")
    print(f"Predictions: {result['predictions']}")
    print(f"Key mode: {result['key_mode']}")
    print(f"Total: {result['total']}")
    print(f"Evaluated: {result['evaluated']}")
    print(f"Missing: {result['missing']}")
    print(f"Invalid: {result['invalid']}")
    accuracy = result["accuracy"]
    print(f"Accuracy: {accuracy:.4f}" if accuracy is not None else "Accuracy: n/a")
    print("Per-answer:")
    for answer, stats in result["per_answer"].items():
        acc = stats["accuracy"]
        acc_text = f"{acc:.4f}" if acc is not None else "n/a"
        print(
            f"  {answer}: {stats['correct']}/{stats['evaluated']} "
            f"evaluated, {stats['total']} total, acc={acc_text}"
        )


if __name__ == "__main__":
    main()
