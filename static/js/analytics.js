document.addEventListener("DOMContentLoaded", function () {

    let heartChart = null;
    let spo2Chart = null;
    let confidenceChart = null;


    /* =====================================================
       COMMON CHART OPTIONS
    ===================================================== */

    const commonOptions = {

        responsive: true,

        maintainAspectRatio: false,

        interaction: {
            intersect: false,
            mode: "index"
        },

        plugins: {

            legend: {
                labels: {
                    color: "#ffffff"
                }
            }

        },

        scales: {

            x: {

                ticks: {
                    color: "#7f8a9c"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }

            },

            y: {

                ticks: {
                    color: "#7f8a9c"
                },

                grid: {
                    color: "rgba(255,255,255,0.05)"
                }

            }

        }

    };


    /* =====================================================
       LOAD LIVE ANALYTICS DATA
    ===================================================== */

    async function updateAnalytics() {

        try {

            const response = await fetch(
                "/api/dashboard_data",
                {
                    method: "GET",
                    cache: "no-store"
                }
            );


            if (!response.ok) {

                throw new Error(
                    "API returned " + response.status
                );

            }


            const data = await response.json();


            if (data.status !== "success") {

                console.error(
                    "Analytics API error:",
                    data.message
                );

                return;

            }


            /* =================================================
               GET DATA
            ================================================= */

            const dates =
                data.dates || [];

            const heartRate =
                data.heartRate || [];

            const spo2 =
                data.spo2 || [];


            /* =================================================
               CONFIDENCE FROM AI RESULT
            ================================================= */

            const predictionDates =
    data.predictionDates || [];

const confidence =
    data.confidence || [];

            /* =================================================
               HEART RATE CHART
            ================================================= */

            const heartCanvas =
                document.getElementById("heartChart");


            if (heartCanvas) {

                if (heartChart) {

                    heartChart.destroy();

                }


                heartChart = new Chart(
                    heartCanvas,
                    {

                        type: "line",

                        data: {

                            labels: predictionDates,

                            datasets: [

                                {

                                    label:
                                        "Heart Rate",

                                    data:
                                        heartRate,

                                    borderColor:
                                        "#ff3b81",

                                    backgroundColor:
                                        "rgba(255,59,129,0.08)",

                                    borderWidth: 3,

                                    fill: true,

                                    tension: 0.35,

                                    pointRadius: 4,

                                    pointHoverRadius: 7

                                }

                            ]

                        },

                        options: commonOptions

                    }
                );

            }


            /* =================================================
               SPO2 CHART
            ================================================= */

            const spo2Canvas =
                document.getElementById("spo2Chart");


            if (spo2Canvas) {

                if (spo2Chart) {

                    spo2Chart.destroy();

                }


                spo2Chart = new Chart(
                    spo2Canvas,
                    {

                        type: "line",

                        data: {

                            labels: predictionDates,

                            datasets: [

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

                                    pointHoverRadius: 7

                                }

                            ]

                        },

                        options: {

                            ...commonOptions,

                            scales: {

                                ...commonOptions.scales,

                                y: {

                                    ...commonOptions.scales.y,

                                    min: 80,

                                    max: 100

                                }

                            }

                        }

                    }
                );

            }


            /* =================================================
               CONFIDENCE CHART
            ================================================= */

            const confidenceCanvas =
                document.getElementById(
                    "confidenceChart"
                );


            if (confidenceCanvas) {

                if (confidenceChart) {

                    confidenceChart.destroy();

                }


                confidenceChart = new Chart(
                    confidenceCanvas,
                    {

                        type: "bar",

                        data: {

                            labels: predictionDates,

                            datasets: [

                                {

                                    label:
                                        "AI Confidence",

                                    data:
                                        confidence,

                                    backgroundColor:
                                        "rgba(180,119,255,0.65)",

                                    borderColor:
                                        "#b477ff",

                                    borderWidth: 1,

                                    borderRadius: 8

                                }

                            ]

                        },

                        options: {

                            ...commonOptions,

                            scales: {

                                ...commonOptions.scales,

                                y: {

                                    ...commonOptions.scales.y,

                                    min: 0,

                                    max: 100

                                }

                            }

                        }

                    }
                );

            }


            console.log(
                "Analytics updated:",
                new Date().toLocaleTimeString()
            );

        }


        catch (error) {

            console.error(
                "Analytics update failed:",
                error
            );

        }

    }


    /* =====================================================
       FIRST LOAD
    ===================================================== */

    updateAnalytics();


    /* =====================================================
       AUTO REFRESH EVERY 10 SECONDS
    ===================================================== */

    setInterval(
        updateAnalytics,
        10000
    );

});