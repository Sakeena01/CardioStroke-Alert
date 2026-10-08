from flask import Blueprint, render_template

health3d_bp = Blueprint("health3d", __name__)

@health3d_bp.route("/health3d")
def health3d():
    return render_template("health3d.html")