const API_URL = "http://127.0.0.1:5000/predict";

async function fetchPrediction() {
    const res = await fetch(API_URL + "?t=" + Date.now());

    const data = await res.json();

    const up = Math.round(data.probability.up * 100);
    const down = Math.round(data.probability.down * 100);

    document.getElementById("upBar").style.width = up + "%";
    document.getElementById("downBar").style.width = down + "%";

    document.getElementById("upValue").innerText = up + "%";
    document.getElementById("downValue").innerText = down + "%";

    const biasEl = document.getElementById("bias");
    biasEl.innerText = data.bias;

    if (data.bias === "UP") biasEl.style.background = "#22c55e";
    else if (data.bias === "DOWN") biasEl.style.background = "#ef4444";
    else biasEl.style.background = "#64748b";

    document.getElementById("confidence").innerText =
        "Confidence: " + data.confidence;

    document.getElementById("recommendation").innerText =
        data.recommendation;
}

fetchPrediction();
// Auto refresh every 10 seconds
setInterval(fetchPrediction, 10000);
