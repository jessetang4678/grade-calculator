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


def score_needed_on_final(current, final_weight, target):
    """Return the score needed on the final to finish the course with `target`.

    `current` is the grade so far (0-100) on everything except the final,
    `final_weight` is how much the final counts (in %, above 0 and up to 100),
    and `target` is the course grade wanted (0-100).

    The answer can be above 100 (the target is out of reach) or 0 or below
    (the target is already secured).
    """
    if not 0 <= current <= 100:
        raise ValueError(f"Your current grade must be between 0 and 100 (got {current:g}).")
    if not 0 <= target <= 100:
        raise ValueError(f"The target grade must be between 0 and 100 (got {target:g}).")
    if not 0 < final_weight <= 100:
        raise ValueError(f"The final's weight must be above 0 and at most 100 (got {final_weight:g}).")

    share = final_weight / 100
    return (target - current * (1 - share)) / share
