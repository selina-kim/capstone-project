"""
Generates a larger synthetic review log CSV for use in the optimizer split tests.

Simulates 5,000 cards over ~18 months using the FSRS Scheduler with realistic
grade distributions, producing enough review events for the 80/10/10 train/val/test
split to be statistically meaningful (~500+ reviews per split).

Run from inside the Docker container:
    docker compose exec backend python3 src/tests/sample_data/generate_large_sample_logs.py

"""

import sys
import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, "src")

from services.fsrs.scheduler import Scheduler
from services.fsrs.card import Card
from services.fsrs.grade import Grade
from services.fsrs.learning_state import LearningState

OUTPUT_PATH = Path("src/tests/sample_data/large_sample_logs.csv")

NUM_CARDS = 5_000
START_DATE = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
END_DATE   = datetime(2025, 6, 30, 0, 0, 0, tzinfo=timezone.utc)

# Realistic grade distribution: most cards graded Good, some Again, fewer Hard/Easy
FIRST_GRADE_WEIGHTS = {
    Grade.Again: 0.20,
    Grade.Hard:  0.15,
    Grade.Good:  0.55,
    Grade.Easy:  0.10,
}
SUBSEQUENT_GRADE_WEIGHTS = {
    Grade.Again: 0.10,
    Grade.Hard:  0.20,
    Grade.Good:  0.55,
    Grade.Easy:  0.15,
}

# Realistic review durations in ms per grade
REVIEW_DURATION_RANGES = {
    Grade.Again: (8_000,  25_000),
    Grade.Hard:  (6_000,  18_000),
    Grade.Good:  (3_000,  12_000),
    Grade.Easy:  (1_500,   6_000),
}


def pick_grade(weights: dict[Grade, float], rng: random.Random) -> Grade:
    grades = list(weights.keys())
    w = [weights[g] for g in grades]
    return rng.choices(grades, weights=w, k=1)[0]


def simulate_card(
    card_id: int,
    scheduler: Scheduler,
    rng: random.Random,
) -> list[dict]:
    rows = []
    card = Card(card_id=str(card_id), due=START_DATE)
    current_date = START_DATE
    first_review = True

    while current_date < END_DATE:
        grade = pick_grade(
            FIRST_GRADE_WEIGHTS if first_review else SUBSEQUENT_GRADE_WEIGHTS, rng
        )
        first_review = False

        lo, hi = REVIEW_DURATION_RANGES[grade]
        duration_ms = rng.randint(lo, hi)

        card, review_log = scheduler.review_card(
            card=card,
            grade=grade,
            review_datetime=current_date,
            review_duration=duration_ms,
        )

        rows.append({
            "card_id": card_id,
            "grade": grade.value,
            "review_datetime": current_date.isoformat(),
            "review_duration": duration_ms,
        })

        current_date = card.due

    return rows


def main():
    rng = random.Random(42)
    scheduler = Scheduler(enable_fuzzing=False)

    all_rows = []
    for i in range(NUM_CARDS):
        card_id = 1_000_000_000 + i
        rows = simulate_card(card_id=card_id, scheduler=scheduler, rng=rng)
        all_rows.extend(rows)
        if (i + 1) % 500 == 0:
            print(f"  {i + 1}/{NUM_CARDS} cards simulated ({len(all_rows)} reviews so far)")

    # sort by review_datetime (mimics real export order)
    all_rows.sort(key=lambda r: r["review_datetime"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["card_id", "grade", "review_datetime", "review_duration"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone. {len(all_rows)} reviews across {NUM_CARDS} cards written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
