function getStock() {
    const symbol = document.getElementById("symbolInput").value;

    // Show loading immediately
    document.getElementById("result").innerText = "Loading...";

    fetch(`http://127.0.0.1:8000/stock/${symbol}`)
        .then(response => response.json())
        .then(data => {
            if(data.price) {
                document.getElementById("result").innerText =
                    `Price of ${data.symbol}: ${data.price} ${data.currency}`;
            } else {
                document.getElementById("result").innerText =
                    `Stock symbol "${data.symbol}" not found`;
            }
        })
        .catch(error => {
            document.getElementById("result").innerText = "Error fetching data";
            console.error(error);
        });

        loadChart(symbol);



}


function loadHistory() {
    fetch("http://127.0.0.1:8000/history")
        .then(response => response.json())
        .then(data => {
            const historyDiv = document.getElementById("history");
            historyDiv.innerHTML = "";

            data.forEach(item => {
                const p = document.createElement("p");
                p.innerText = `${item.symbol} - ${item.price} USD - ${item.time}`;
                historyDiv.appendChild(p);
            });
        });
}

window.onload = function () {
    loadHistory();
};

let priceChart = null; // will store the chart instance

function loadChart(symbol) {
    fetch(`http://127.0.0.1:8000/stock/${symbol}/history`)
        .then(response => response.json())
        .then(data => {

            const dates = data.map(item => item.date);
            const prices = data.map(item => item.price);

            const ctx = document.getElementById("priceChart").getContext("2d");

            // If chart already exists, destroy it before creating a new one
            if (priceChart) {
                priceChart.destroy();
            }

            priceChart = new Chart(ctx, {
                type: "line",
                data: {
                    labels: dates,
                    datasets: [{
                        label: "Price (USD)",
                        data: prices,
                        borderWidth: 2,
                        tension: 0.3
                    }]
                }
            });
        });
}


