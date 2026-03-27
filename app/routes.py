from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os
import csv
from datetime import datetime

routes = Blueprint("routes", __name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

states_path = os.path.join(BASE_DIR, "data", "states.csv")
score_file = os.path.join(BASE_DIR, "data", "scores.csv")

data = pd.read_csv(states_path)

guessed_states = []
attempts = 0
start_time = datetime.now()


@routes.route("/")
def home():
    return render_template("index.html")


@routes.route("/guess", methods=["POST"])
def guess():
    global attempts
    attempts += 1

    req = request.get_json()

    guessed = req.get("guessed")
    clicked = req.get("clicked")

    if not guessed or not clicked:
        return jsonify({"correct": False})

    guessed_clean = guessed.strip().lower()
    clicked_clean = clicked.strip().lower()

    states_lower = [s.lower() for s in data["state"].values]
    guessed_states_lower = [s.lower() for s in guessed_states]

    if (
        guessed_clean == clicked_clean and
        guessed_clean in states_lower and
        guessed_clean not in guessed_states_lower
    ):
        guessed_states.append(clicked.strip())

        return jsonify({
            "correct": True,
            "score": len(guessed_states)
        })

    return jsonify({"correct": False})


@routes.route("/finish", methods=["POST"])
def finish():
    name = request.json.get("name")

    end_time = datetime.now()
    time_taken = (end_time - start_time).seconds

    file_exists = os.path.isfile(score_file)

    with open(score_file, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Name", "Score", "Total_Attempts", "Time_Taken", "Date"])

        writer.writerow([
            name,
            len(guessed_states),
            attempts,
            time_taken,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

    return jsonify({"message": "Saved"})