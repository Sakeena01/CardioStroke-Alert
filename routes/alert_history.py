from flask import Blueprint, render_template

from models.user import User
from models.health_alert import HealthAlert


alert_history_bp = Blueprint(
    "alert_history",
    __name__
)


@alert_history_bp.route("/alert-history")
def alert_history():

    # ---------------------------------------------------------
    # Get current user
    # ---------------------------------------------------------

    user = User.query.first()


    # ---------------------------------------------------------
    # No user available
    # ---------------------------------------------------------

    if user is None:

        return render_template(
            "alert_history.html",
            user=None,
            alerts=[]
        )


    # ---------------------------------------------------------
    # Get user's alerts
    # ---------------------------------------------------------

    alerts = (
        HealthAlert.query
        .filter(
            HealthAlert.user_id == user.id
        )
        .order_by(
            HealthAlert.sent_at.desc()
        )
        .all()
    )


    # ---------------------------------------------------------
    # Render page
    # ---------------------------------------------------------

    return render_template(
        "alert_history.html",
        user=user,
        alerts=alerts
    )