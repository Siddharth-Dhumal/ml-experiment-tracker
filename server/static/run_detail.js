(function () {
    const card = document.getElementById("chart-card");
    if (!card) return;

    const runId = card.getAttribute("data-run-id");
    const metricNamesJson = card.getAttribute("data-metric-names") || "[]";
    let metricNames = [];
    try { metricNames = JSON.parse(metricNamesJson); } catch { metricNames = []; }

    const select = document.getElementById("metricSelect");
    const canvas = document.getElementById("metricChart");
    if (!select || !canvas || metricNames.length === 0) return;

    metricNames.forEach((name) => {
        const opt = document.createElement("option");
        opt.value = name;
        opt.textContent = name;
        select.appendChild(opt);
    });

    let chart = null;

    async function loadMetric(name) {
        const url = `/api/runs/${runId}/metrics?name=${encodeURIComponent(name)}&limit=2000`;
        const resp = await fetch(url);
        const data = await resp.json();

        const labels = data.map((m) => m.step);
        const values = data.map((m) => m.value);

        if (chart) chart.destroy();

        chart = new Chart(canvas.getContext("2d"), {
            type: "line",
            data: {
                labels,
                datasets: [{ label: name, data: values }]
            },
            options: {
                responsive: true,
                animation: false,
                scales: {
                    x: { title: { display: true, text: "step" } },
                    y: { title: { display: true, text: "value" } }
                }
            }
        });
    }

    select.addEventListener("change", () => loadMetric(select.value));
    loadMetric(select.value);
})();