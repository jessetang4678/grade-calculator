from flask import Flask, render_template, request

from grades import letter_grade, score_needed_on_final, weighted_average

app = Flask(__name__)

ROWS = 5  # how many assignment rows the form shows


def read_assignments(form):
    """Turn the submitted form into (name, score, weight) rows, skipping blank rows."""
    rows = []
    names = form.getlist("name")
    scores = form.getlist("score")
    weights = form.getlist("weight")
    for name, score, weight in zip(names, scores, weights):
        name, score, weight = name.strip(), score.strip(), weight.strip()
        if not (name or score or weight):
            continue  # a completely empty row is ignored
        if not score or not weight:
            raise ValueError("Each assignment needs both a score and a weight.")
        try:
            rows.append((name, float(score), float(weight)))
        except ValueError:
            raise ValueError("Scores and weights must be numbers.")
    return rows


def read_number(form, field, label):
    """Read one number from the form, with a readable error if it is missing or not a number."""
    value = form.get(field, "").strip()
    if not value:
        raise ValueError(f"Enter {label}.")
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"{label.capitalize()} must be a number.")


def final_message(needed, target):
    """Describe the score needed on the final in plain words."""
    if needed > 100:
        return f"You would need {needed:.1f}% on the final, so {target:g}% is out of reach."
    if needed <= 0:
        return f"You have already secured {target:g}%, even with 0 on the final."
    return f"You need {needed:.1f}% on the final to finish with {target:g}%."


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    final_result = None
    final_error = None
    entries = [{"name": "", "score": "", "weight": ""} for _ in range(ROWS)]
    final_inputs = {"current": "", "final_weight": "", "target": ""}

    if request.method == "POST" and request.form.get("form") == "final":
        # The "What do I need on the final?" form.
        final_inputs = {key: request.form.get(key, "") for key in final_inputs}
        try:
            current = read_number(request.form, "current", "your current grade")
            final_weight = read_number(request.form, "final_weight", "the final's weight")
            target = read_number(request.form, "target", "the target grade")
            needed = score_needed_on_final(current, final_weight, target)
            final_result = final_message(needed, target)
        except ValueError as exc:
            final_error = str(exc)

    elif request.method == "POST":
        # The weighted grade form.
        # Keep what the user typed so the form is not wiped on submit.
        submitted = zip(
            request.form.getlist("name"),
            request.form.getlist("score"),
            request.form.getlist("weight"),
        )
        for i, (name, score, weight) in enumerate(submitted):
            if i < ROWS:
                entries[i] = {"name": name, "score": score, "weight": weight}

        try:
            rows = read_assignments(request.form)
            final = weighted_average([(score, weight) for _, score, weight in rows])
            result = {"final": round(final, 2), "letter": letter_grade(final)}
        except ValueError as exc:
            error = str(exc)

    return render_template(
        "index.html",
        entries=entries,
        result=result,
        error=error,
        final_inputs=final_inputs,
        final_result=final_result,
        final_error=final_error,
    )


if __name__ == "__main__":
    app.run(debug=True)
