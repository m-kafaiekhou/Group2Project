let salesCtx = document.getElementById("salesChart").getContext("2d");
let salesChart = new Chart(salesCtx, {
    type: "bar",
    options: {
        responsive: true,
        title: {
            display: false,
            text: ""
        }
    }
});
let spendPerCustomerCtx = document.getElementById("spendPerCustomerChart").getContext("2d");
let spendPerCustomerChart = new Chart(spendPerCustomerCtx, {
    type: "line",
    options: {
        responsive: true,
        title: {
            display: false,
            text: ""
        }
    }
});
let paymentSuccessCtx = document.getElementById("paymentSuccessChart").getContext("2d");
let paymentSuccessChart = new Chart(paymentSuccessCtx, {
    type: "pie",
    options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1,
        title: {
            display: false,
            text: ""
        },
        layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 25
            }
        }
    }
});
let paymentMethodCtx = document.getElementById("paymentMethodChart").getContext("2d");
let paymentMethodChart = new Chart(paymentMethodCtx, {
    type: "pie",
    options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1,
        title: {
            display: false,
            text: ""
        },
        layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 25
            }
        }
    }
});

// JSON response part
window.onload = loadAllCharts
window.onclick = loadAllCharts

function loadChart(chart, endpoint) {
    $.ajax({
        url: endpoint,
        type: "GET",
        dataType: "json",
        success: (jsonResponse) => {
            // Extract data from the response
            const title = jsonResponse.title;
            const labels = jsonResponse.data.labels;
            const datasets = jsonResponse.data.datasets;

            // Reset the current chart
            chart.data.datasets = [];
            chart.data.labels = [];

            // Load new data into the chart
            chart.options.title.text = title;
            chart.options.title.display = true;
            chart.data.labels = labels;
            datasets.forEach(dataset => {
                chart.data.datasets.push(dataset);
            });
            chart.update();
        },
        error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
    });
}

function loadAllCharts() {
    loadChart(salesChart, `/dashboard/chart/sales/this-year/`);
    loadChart(spendPerCustomerChart, `/dashboard/chart/sales/this-month/`);
    loadChart(paymentSuccessChart, `/dashboard/chart/sales/this-year/`);
    loadChart(paymentMethodChart, `/dashboard/chart/sales/this-month/`);
}