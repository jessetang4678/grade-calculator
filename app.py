from flask import Flask, render_template, request

from grades import letter_grade, weighted_average

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


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    entries = [{"name": "", "score": "", "weight": ""} for _ in range(ROWS)]

    if request.method == "POST":
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

    return render_template("index.html", entries=entries, result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
