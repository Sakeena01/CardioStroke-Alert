async function updateDashboard() {

    const response = await fetch("/api/latest");
    const data = await response.json();

    document.getElementById("heartRate").innerHTML = data.heart_rate + " BPM";
    document.getElementById("spo2").innerHTML = data.spo2 + " %";
    document.getElementById("steps").innerHTML = data.steps;
    document.getElementById("glucose").innerHTML = data.glucose;
    document.getElementById("bmi").innerHTML = data.bmi;
    document.getElementById("prediction").innerHTML = data.prediction;
    document.getElementById("confidence").innerHTML =
        data.confidence + "%";
}
const scoreCircleElement =
    document.querySelector(
        "[data-health='score-circle']"
    );

if (scoreCircleElement) {

    scoreCircleElement.textContent =
        data.health_score;
}
/* =================================================
   AI RISK
================================================= */

const riskElement =
    document.querySelector(
        "[data-ai='risk']"
    );

if (riskElement) {

    riskElement.textContent =
        data.ai.risk;


    /* Remove previous risk classes */

    riskElement.classList.remove(
        "low-risk",
        "high-risk"
    );


    /* Apply correct risk class */

    if (data.ai.risk === "High Risk") {

        riskElement.classList.add(
            "high-risk"
        );

    } else {

        riskElement.classList.add(
            "low-risk"
        );
    }
}


/* =================================================
   AI CONFIDENCE
================================================= */

const confidenceElement =
    document.querySelector(
        "[data-ai='confidence']"
    );

if (confidenceElement) {

    confidenceElement.textContent =
        data.ai.confidence + "%";
}


/* =================================================
   STROKE PROBABILITY
================================================= */

const strokeElement =
    document.querySelector(
        "[data-ai='stroke-probability']"
    );

if (strokeElement) {

    strokeElement.textContent =
        data.ai.stroke_probability + "%";
}


/* =================================================
   NORMAL PROBABILITY
================================================= */

const normalElement =
    document.querySelector(
        "[data-ai='normal-probability']"
    );

if (normalElement) {

    normalElement.textContent =
        data.ai.normal_probability + "%";
}
updateDashboard();

setInterval(updateDashboard, 300000);