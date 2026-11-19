"""The grade math, kept separate from the web code so it is easy to test."""

LETTER_CUTOFFS = [(90, "A"), (80, "B"), (70, "C"), (60, "D")]


def letter_grade(percent):
    """Return the letter grade for a percentage: 90+ A, 80+ B, 70+ C, 60+ D, else F."""
    for cutoff, letter in LETTER_CUTOFFS:
        if percent >= cutoff:
            return letter
    return "F"


def weighted_average(assignments):
    """Return the weighted final grade for a list of (score, weight) pairs.

    Scores are percentages from 0 to 100. Weights are percentages and must
    add up to 100. Raises ValueError with a readable message otherwise.
    """
    if not assignments:
        raise ValueError("Enter at least one assignment.")

    for score, weight in assignments:
        if not 0 <= score <= 100:
            raise ValueError(f"Scores must be between 0 and 100 (got {score:g}).")
        if weight <= 0:
            raise ValueError(f"Weights must be greater than 0 (got {weight:g}).")

    total_weight = sum(weight for _, weight in assignments)
    if abs(total_weight - 100) > 0.01:
        raise ValueError(f"Weights must add up to 100% (they add up to {total_weight:g}%).")

    return sum(score * weight for score, weight in assignments) / 100
