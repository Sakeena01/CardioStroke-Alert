// Heart Rate Chart
new Chart(document.getElementById("heartChart"), {
    type: "line",
    data: {
        labels: chartData.labels,
        datasets: [{
            label: "Heart Rate",
            data: chartData.heartData,
            borderColor: "#00D9FF",
            backgroundColor: "rgba(0,217,255,0.3)",
            fill: true,
            tension: 0.4,
            pointBackgroundColor: "#FF007F",   // colorful points
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// SpO₂ Chart
new Chart(document.getElementById("spo2Chart"), {
    type: "line",
    data: {
        labels: chartData.labels,
        datasets: [{
            label: "SpO₂",
            data: chartData.spo2Data,
            borderColor: "#00FF99",
            backgroundColor: "rgba(0,255,153,0.3)",
            fill: true,
            tension: 0.4,
            pointBackgroundColor: "#FFD700",   // golden points
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
});

// Confidence Chart
new Chart(document.getElementById("confidenceChart"), {
    type: "bar",
    data: {
        labels: chartData.labels,
        datasets: [{
            label: "Confidence (%)",
            data: chartData.confidenceData,
            backgroundColor: [
                "#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#FFD700"
            ], // colorful bars
            borderRadius: 8
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                max: 100
            }
        }
    }
});
