import pytest

from app import app
from grades import letter_grade, score_needed_on_final, weighted_average


# ---- The grade math (grades.py) ----

def test_weighted_average_of_two_equal_weights():
    assert weighted_average([(90, 50), (80, 50)]) == 85


def test_weighted_average_respects_weights():
    # 100 counts for 80% and 50 counts for 20%: 80 + 10 = 90
    assert weighted_average([(100, 80), (50, 20)]) == 90


def test_letter_grade_cutoffs():
    assert letter_grade(95) == "A"
    assert letter_grade(90) == "A"
    assert letter_grade(89.99) == "B"
    assert letter_grade(80) == "B"
    assert letter_grade(70) == "C"
    assert letter_grade(60) == "D"
    assert letter_grade(59.99) == "F"


def test_weights_must_add_up_to_100():
    with pytest.raises(ValueError, match="add up to 100"):
        weighted_average([(90, 50), (80, 40)])


def test_scores_must_be_between_0_and_100():
    with pytest.raises(ValueError, match="between 0 and 100"):
        weighted_average([(120, 100)])
    with pytest.raises(ValueError, match="between 0 and 100"):
        weighted_average([(-5, 100)])


# ---- The web page (app.py) ----

@pytest.fixture
def client():
    return app.test_client()


def test_homepage_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Grade Calculator" in response.get_data(as_text=True)


def test_form_shows_final_grade(client):
    response = client.post("/", data={
        "name": ["Homework", "Exam"],
        "score": ["90", "80"],
        "weight": ["50", "50"],
    })
    page = response.get_data(as_text=True)
    assert "85.0%" in page
    assert "(B)" in page


def test_form_rejects_text_instead_of_numbers(client):
    response = client.post("/", data={
        "name": ["Homework"],
        "score": ["abc"],
        "weight": ["100"],
    })
    assert "must be numbers" in response.get_data(as_text=True)


# ---- What do I need on the final? ----

def test_score_needed_on_final():
    # 80 so far counts for 50%; to finish with 85 the final (50%) must be 90.
    assert score_needed_on_final(80, 50, 85) == 90
    # 88 so far counts for 75%; to finish with 90 the final (25%) must be 96.
    assert score_needed_on_final(88, 25, 90) == 96


def test_score_needed_on_final_rejects_bad_weight():
    with pytest.raises(ValueError, match="weight"):
        score_needed_on_final(80, 0, 90)
    with pytest.raises(ValueError, match="weight"):
        score_needed_on_final(80, 120, 90)


def test_final_form_shows_needed_score(client):
    response = client.post("/", data={
        "form": "final",
        "current": "88",
        "final_weight": "25",
        "target": "90",
    })
    assert "You need 96.0% on the final" in response.get_data(as_text=True)


def test_final_form_says_when_target_is_out_of_reach(client):
    response = client.post("/", data={
        "form": "final",
        "current": "60",
        "final_weight": "20",
        "target": "90",
    })
    assert "out of reach" in response.get_data(as_text=True)
