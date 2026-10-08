document.addEventListener("DOMContentLoaded", function () {

    let healthChart = null;


    /* =====================================================
       GET DASHBOARD ELEMENTS
    ===================================================== */

    const heartRateElement =
        document.querySelector('[data-health="heart-rate"]');

    const spo2Element =
        document.querySelector('[data-health="spo2"]');

    const stepsElement =
        document.querySelector('[data-health="steps"]');

    const caloriesElement =
        document.querySelector('[data-health="calories"]');

    const distanceElement =
        document.querySelector('[data-health="distance"]');

    const sleepElement =
        document.querySelector('[data-health="sleep"]');


    /* =====================================================
       UPDATE DASHBOARD CARDS
    ===================================================== */

    function updateHealthCards(data) {

        const health = data.health || {};


        if (heartRateElement) {

            heartRateElement.textContent =
                health.heart_rate ?? "--";

        }


        if (spo2Element) {

            spo2Element.textContent =
                health.spo2 ?? "--";

        }


        if (stepsElement) {

            stepsElement.textContent =
                health.steps ?? "--";

        }


        if (caloriesElement) {

            caloriesElement.textContent =
                health.calories ?? "--";

        }


        if (distanceElement) {

            distanceElement.textContent =
                health.distance ?? "--";

        }


        if (sleepElement) {

            sleepElement.textContent =
                health.sleep ?? "--";

        }

    }


    /* =====================================================
       UPDATE HEALTH CHART
    ===================================================== */

    function updateHealthChart(data) {

        const dates =
            data.dates || [];

        const heartRate =
            data.heartRate || [];

        const spo2 =
            data.spo2 || [];


        const canvas =
            document.getElementById("healthChart");


        if (!canvas) {

            console.error(
                "healthChart canvas not found"
            );

            return;

        }


        /* =================================================
           CREATE CHART ONLY ONCE
        ================================================= */

        if (!healthChart) {

            const ctx =
                canvas.getContext("2d");


            healthChart =
                new Chart(ctx, {

                    type: "line",

                    data: {

                        labels: dates,

                        datasets: [

                            {

                                label:
                                    "Heart Rate",

                                data:
                                    heartRate,

                                borderColor:
                                    "#ff3b81",

                                backgroundColor:
                                    "rgba(255,59,129,0.10)",

                                borderWidth: 3,

                                fill: true,

                                tension: 0.35,

                                pointRadius: 4,

                                pointHoverRadius: 6

                            },


                            {

                                label:
                                    "SpO₂",

                                data:
                                    spo2,

                                borderColor:
                                    "#00e5ff",

                                backgroundColor:
                                    "rgba(0,229,255,0.08)",

                                borderWidth: 3,

                                fill: true,

                                tension: 0.35,

                                pointRadius: 4,

                                pointHoverRadius: 6

                            }

                        ]

                    },


                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        interaction: {

                            intersect: false,

                            mode: "index"

                        },


                        plugins: {

                            legend: {

                                display: true,

                                labels: {

                                    color: "#ffffff",

                                    usePointStyle: true

                                }

                            }

                        },


                        scales: {

                            x: {

                                ticks: {

                                    color:
                                        "#7f8a9c"

                                },

                                grid: {

                                    color:
                                        "rgba(255,255,255,0.05)"

                                }

                            },


                            y: {

                                ticks: {

                                    color:
                                        "#7f8a9c"

                                },

                                grid: {

                                    color:
                                        "rgba(255,255,255,0.05)"

                                }

                            }

                        }

                    }

                });


        }

        /* =================================================
           UPDATE EXISTING CHART
        ================================================= */

        else {

            healthChart.data.labels =
                dates;


            healthChart.data.datasets[0].data =
                heartRate;


            healthChart.data.datasets[1].data =
                spo2;


            healthChart.update("none");

        }

    }


    /* =====================================================
       UPDATE RISK PANEL
    ===================================================== */

    function updateRisk(data) {

        const ai =
            data.ai || {};


        const riskElements =
            document.querySelectorAll(
                "[data-risk]"
            );


        riskElements.forEach(
            function (element) {

                if (ai.risk) {

                    element.textContent =
                        ai.risk;

                }

            }
        );


        const confidenceElements =
            document.querySelectorAll(
                "[data-confidence]"
            );


        confidenceElements.forEach(
            function (element) {

                if (
                    ai.confidence !== undefined
                ) {

                    element.textContent =
                        ai.confidence + "%";

                }

            }
        );

    }


    /* =====================================================
       UPDATE HEALTH SCORE
    ===================================================== */

    function updateHealthScore(data) {

        const score =
            Number(
                data.health_score ?? 0
            );


        const scoreElement =
            document.querySelector(
                ".health-score-number"
            );


        const gaugeElement =
            document.querySelector(
                ".health-gauge"
            );


        if (scoreElement) {

            scoreElement.textContent =
                Math.round(score);

        }


        if (gaugeElement) {

            gaugeElement.style.setProperty(
                "--score",
                Math.round(score) + "%"
            );

        }

    }


    /* =====================================================
       FETCH LIVE DATA
    ===================================================== */

    async function updateDashboard() {

        try {

            const response =
                await fetch(
                    "/api/dashboard_data",
                    {
                        method: "GET",
                        cache: "no-store"
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Dashboard API returned " +
                    response.status
                );

            }


            const data =
                await response.json();


            if (data.status !== "success") {

                console.error(
                    "Dashboard API error:",
                    data.message
                );

                return;

            }


            /* =============================================
               UPDATE EVERYTHING
            ============================================== */

            updateHealthCards(data);

            updateHealthChart(data);

            updateRisk(data);

            updateHealthScore(data);


            console.log(
                "Dashboard updated:",
                new Date().toLocaleTimeString()
            );

        }


        catch (error) {

            console.error(
                "Dashboard update failed:",
                error
            );

        }

    }


    /* =====================================================
       FIRST LOAD
    ===================================================== */

    updateDashboard();


    /* =====================================================
       AUTO REFRESH
       Every 10 seconds
    ===================================================== */

    setInterval(
        updateDashboard,
        10000
    );

});