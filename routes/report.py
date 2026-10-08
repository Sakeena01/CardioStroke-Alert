from flask import Blueprint, send_file
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from models.prediction_history import PredictionHistory


report_bp = Blueprint("report", __name__)


@report_bp.route("/report/download")
def download_report():

    records = PredictionHistory.query.order_by(
        PredictionHistory.created_at.desc()
    ).all()

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            "CardioStroke AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Heart & Stroke Health Report",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 20))


    if not records:

        story.append(
            Paragraph(
                "No prediction records are available.",
                styles["Normal"]
            )
        )

    else:

        latest = records[0]

        story.append(
            Paragraph(
                "Latest Health Assessment",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 10))


        latest_data = [

            ["Parameter", "Value"],

            ["Age", str(latest.age)],

            ["Heart Rate",
             f"{latest.heart_rate} BPM"],

            ["SpO₂",
             f"{latest.spo2}%"],

            ["Glucose",
             str(latest.glucose)],

            ["BMI",
             str(latest.bmi)],

            ["Steps",
             str(latest.steps)],

            ["Prediction",
             str(latest.prediction)],

            ["Confidence",
             f"{latest.confidence}%"]

        ]


        table = Table(
            latest_data,
            colWidths=[200, 250]
        )


        table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#111827")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ])
        )


        story.append(table)

        story.append(Spacer(1, 25))


        story.append(
            Paragraph(
                "Prediction History",
                styles["Heading2"]
            )
        )

        story.append(Spacer(1, 10))


        history_data = [[
            "Date",
            "Heart Rate",
            "SpO₂",
            "BMI",
            "Result",
            "Confidence"
        ]]


        for record in records[:20]:

            history_data.append([

                record.created_at.strftime(
                    "%d/%m/%Y"
                ),

                str(record.heart_rate),

                str(record.spo2),

                str(record.bmi),

                str(record.prediction),

                f"{record.confidence}%"

            ])


        history_table = Table(
            history_data,
            repeatRows=1
        )


        history_table.setStyle(
            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#111827")
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )

            ])
        )


        story.append(history_table)


    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "Generated by CardioStroke AI Health Monitoring System.",
            styles["Normal"]
        )
    )


    document.build(story)

    buffer.seek(0)


    return send_file(
        buffer,
        as_attachment=True,
        download_name="CardioStroke_AI_Report.pdf",
        mimetype="application/pdf"
    )