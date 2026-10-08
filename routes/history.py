from flask import Blueprint, render_template

from models.prediction_history import PredictionHistory


history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
def history():

    records = PredictionHistory.query.order_by(
        PredictionHistory.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        records=records
    )