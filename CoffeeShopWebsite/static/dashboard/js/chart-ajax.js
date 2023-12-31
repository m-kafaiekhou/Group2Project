// // JSON response part
window.onload = loadAllCharts

// window.onclick = loadAllCharts

function convertChartDataToCSV(args) {
    let result, columnDelimiter, lineDelimiter, labels, data;

    data = args.data || null;
    if (data == null || !data.length) {
        return null;
    }

    labels = args.labels || null;
    if (labels == null || !labels.length) {
        return null;
    }

    columnDelimiter = args.columnDelimiter || ',';
    lineDelimiter = args.lineDelimiter || '\n';

    result = '';
    result += labels.join(columnDelimiter);
    result += lineDelimiter;

    for (let i = 0; i < data.length; i++) {
        result += data[i];
        result += columnDelimiter;
    }

    return result;
}

function downloadCSV(chart) {
    var dataLabels = chart.data.labels;
    var datasets = chart.data.datasets;
    var csv = '';

    for (var i = 0; i < datasets.length; i++) {
        var datasetCSV = convertChartDataToCSV({
            data: datasets[i].data,
            labels: dataLabels,
            columnDelimiter: ',',
            lineDelimiter: '\n'
        });
        csv += datasetCSV;
    }

    if (csv == null) return;

    var filename = 'chart-data.csv';
    var csvData = new Blob([csv], {type: 'text/csv;charset=utf-8;'});

    if (navigator.msSaveBlob) {
        // IE 10+
        navigator.msSaveBlob(csvData, filename);
    } else {
        // Other browsers
        var link = document.createElement('a');
        if (link.download !== undefined) {
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(csvData);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

// function downloadChart(chart) {
//     const imageUrl = chart.toBase64Image();
//
//     const link = document.createElement('a');
//     link.href = imageUrl;
//     link.download = 'chart.png';
//
//     link.click();
// }


function loadChart(chart, endpoint, dnld, start_date = null, end_date = null) {
    $.ajax({
        url: endpoint,
        type: "GET",
        data: {
            start_date: start_date,
            end_date: end_date
        },
        dataType: "json",
        success: (jsonResponse) => {
            const title = jsonResponse.title;
            const labels = jsonResponse.data.labels;
            const datasets = jsonResponse.data.datasets;

            chart.data.datasets = [];
            chart.data.labels = [];

            chart.options.title = title;
            chart.options.title.display = true;
            chart.data.labels = labels;
            datasets.forEach(dataset => {
                chart.data.datasets.push(dataset);
            });

            chart.update();

            document.getElementById(dnld).addEventListener("click", () => {
                downloadCSV(chart)
            });
        },
        error: () => console.log("Failed to fetch chart data from " + endpoint + "!")
    });
}

function loadAllCharts(BigMainChart, BigMainChart2, chartSMCenterup, chartSMLeftup, chartSMRightup, chartSMLEFTdown, chartSMCenterdown, chartSMRightdown, BigMainChart3, mdChartLeft, mdChartRight) {
    loadChart(BigMainChart, links["day-sales"], "dnld-big1");
    loadChart(BigMainChart2, links["top-selling"], "dnld-big2");
    loadChart(chartSMCenterup, links["sale-status-d"], "dnld-scu");
    loadChart(chartSMLeftup, links["sale-status-a"], "dnld-slu");
    loadChart(chartSMRightup, links["sale-status-c"], "dnld-sru");
    loadChart(chartSMLEFTdown, links["peak-hour"], "dnld-sld");
    loadChart(chartSMCenterdown, links["sale-cat"], "dnld-scd");
    loadChart(chartSMRightdown, links["best-customer"], "dnld-srd");
    loadChart(BigMainChart3, links["popular-items"], "dnld-big3");
    loadChart(mdChartLeft, links["sales-by-timeOf-day"], "dnld-ddl");
    loadChart(mdChartRight, links["sales-by-employee"], "dnld-ddr");
}

links = {
    'year-sales': `/dashboard/chart/sales/this-year/`,
    'month-sales': `/dashboard/chart/sales/this-month/`,
    'day-sales': `/dashboard/chart/sales/this-day/`,
    'top-selling': `/dashboard/chart/sales/top-selling/`,
    'sale-cat': `/dashboard/chart/sales/category-sale/`,
    'sale-status-c': `/dashboard/chart/sales/status/C/`,
    'sale-status-d': `/dashboard/chart/sales/status/D/`,
    'sale-status-a': `/dashboard/chart/sales/status/A/`,
    'best-customer': `/dashboard/chart/sales/best-customers/`,
    'peak-hour': `/dashboard/chart/sales/peak-hour/`,
    'popular-items': `/dashboard/chart/sales/popular-items/`,
    'sales-by-timeOf-day': '/dashboard/chart/sales/daily-time-sale/',
    'sales-by-employee': '/dashboard/chart/sales/employee-sales/',
}

type = ['primary', 'info', 'success', 'warning', 'danger'];

demo = {
    initPickColor: function () {
        $('.pick-class-label').click(function () {
            var new_class = $(this).attr('new-class');
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if (display_div.length) {
                var display_buttons = display_div.find('.btn');
                display_buttons.removeClass(old_class);
                display_buttons.addClass(new_class);
                display_div.attr('data-class', new_class);
            }
        });
    },

    initDocChart: function () {
        chartColor = "#FFFFFF";

        // General configuration for the charts with Line gradientStroke
        gradientChartOptionsConfiguration = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },
            tooltips: {
                bodySpacing: 4,
                mode: "nearest",
                intersect: 0,
                position: "nearest",
                xPadding: 10,
                yPadding: 10,
                caretPadding: 10
            },
            responsive: true,
            scales: {
                yAxes: [{
                    display: 0,
                    gridLines: 0,
                    ticks: {
                        display: false
                    },
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawTicks: false,
                        display: false,
                        drawBorder: false
                    }
                }],
                xAxes: [{
                    display: 0,
                    gridLines: 0,
                    ticks: {
                        display: false
                    },
                    gridLines: {
                        zeroLineColor: "transparent",
                        drawTicks: false,
                        display: false,
                        drawBorder: false
                    }
                }]
            },
            layout: {
                padding: {
                    left: 0,
                    right: 0,
                    top: 15,
                    bottom: 15
                }
            }
        };

        ctx = document.getElementById('lineChartExample').getContext("2d");

        gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, '#80b6f4');
        gradientStroke.addColorStop(1, chartColor);

        gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
        gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
        gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");

        myChart = new Chart(ctx, {
            type: 'line',
            responsive: true,
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                datasets: [{
                    label: "Active Users",
                    borderColor: "#f96332",
                    pointBorderColor: "#FFF",
                    pointBackgroundColor: "#f96332",
                    pointBorderWidth: 2,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 1,
                    pointRadius: 4,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: [542, 480, 430, 550, 530, 453, 380, 434, 568, 610, 700, 630]
                }]
            },
            options: gradientChartOptionsConfiguration
        });
    },

    initDashboardPageCharts: function () {

        gradientChartOptionsConfigurationWithTooltipBlue = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.0)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 60,
                        suggestedMax: 125,
                        padding: 20,
                        fontColor: "#2380f7"
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#2380f7"
                    }
                }]
            }
        };

        gradientChartOptionsConfigurationWithTooltipPurple = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.0)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 60,
                        suggestedMax: 125,
                        padding: 20,
                        fontColor: "#9a9a9a"
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(225,78,202,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9a9a9a"
                    }
                }]
            }
        };

        gradientChartOptionsConfigurationWithTooltipOrange = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.0)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 50,
                        suggestedMax: 110,
                        padding: 20,
                        fontColor: "#ff8a76"
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(220,53,69,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#ff8a76"
                    }
                }]
            }
        };

        gradientChartOptionsConfigurationWithTooltipGreen = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            responsive: true,
            scales: {
                yAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.0)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 50,
                        suggestedMax: 125,
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }],

                xAxes: [{
                    barPercentage: 1.6,
                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(0,242,195,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }]
            }
        };


        gradientBarChartConfiguration = {
            maintainAspectRatio: false,
            legend: {
                display: false
            },

            tooltips: {
                backgroundColor: '#f5f5f5',
                titleFontColor: '#333',
                bodyFontColor: '#666',
                bodySpacing: 4,
                xPadding: 12,
                mode: "nearest",
                intersect: 0,
                position: "nearest"
            },
            responsive: true,
            scales: {
                yAxes: [{

                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        suggestedMin: 60,
                        suggestedMax: 120,
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }],

                xAxes: [{

                    gridLines: {
                        drawBorder: false,
                        color: 'rgba(29,140,248,0.1)',
                        zeroLineColor: "transparent",
                    },
                    ticks: {
                        padding: 20,
                        fontColor: "#9e9e9e"
                    }
                }]
            }
        };

        var ctx = document.getElementById("chartLinePurple1").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
        gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

        var data = {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d048b6',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d048b6',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d048b6',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [80, 100, 70, 80, 120, 80],
            }]
        };

        var chartSMLeftup = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipPurple
        });


        var ctxGreen = document.getElementById("chartLineGreen1").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
        gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
        gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

        var data = {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV'],
            datasets: [{
                label: "My First dataset",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#00d6b4',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#00d6b4',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#00d6b4',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [90, 27, 60, 12, 80],
            }]
        };

        let chartSMRightup = new Chart(ctxGreen, {
            type: 'line',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipGreen

        });


        // added charts

        var ctx = document.getElementById("chartLinePurple2").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
        gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

        var data = {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d048b6',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d048b6',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d048b6',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [80, 100, 70, 80, 120, 80],
            }]
        };

        var chartSMLeftdown = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipPurple
        });


        var ctxGreen = document.getElementById("chartLineGreen2").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(66,134,121,0.15)');
        gradientStroke.addColorStop(0.4, 'rgba(66,134,121,0.0)'); //green colors
        gradientStroke.addColorStop(0, 'rgba(66,134,121,0)'); //green colors

        var data = {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV'],
            datasets: [{
                label: "My First dataset",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d048b6',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d048b6',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d048b6',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [90, 27, 60, 12, 80],
            }]
        };

        let chartSMRightdown = new Chart(ctxGreen, {
            type: 'doughnut',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipGreen

        });

        // added charts


        var chart_labels = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        var chart_data = [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100];


        var ctx = document.getElementById("chartBig1").getContext('2d');

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
        gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        var config = {
            type: 'bar',
            data: {
                labels: chart_labels,
                datasets: [{
                    label: "My First dataset",
                    fill: true,
                    backgroundColor: gradientStroke,
                    borderColor: '#d346b1',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#d346b1',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#d346b1',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: chart_data,
                }]
            },
            options: gradientChartOptionsConfigurationWithTooltipPurple
        };
        let BigMainChart = new Chart(ctx, config);
        $("#0").click(function () {
            loadChart(BigMainChart, links["day-sales"], "dnld-big1")
            BigMainChart.update();
        });
        $("#1").click(function () {
            loadChart(BigMainChart, links["month-sales"], "dnld-big1")
            BigMainChart.update();
        });

        $("#2").click(function () {
            loadChart(BigMainChart, links["year-sales"], "dnld-big1")
            BigMainChart.update();
        });

        var ctx2 = document.getElementById("chartBig2").getContext('2d');

        var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

        gradientStroke2.addColorStop(1, 'rgba(72,72,176,0.1)');
        gradientStroke2.addColorStop(0.4, 'rgba(72,72,176,0.0)');
        gradientStroke2.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        var config2 = {
            type: 'bar',
            data: {
                labels: chart_labels,
                datasets: [{
                    label: "My First dataset",
                    fill: true,
                    backgroundColor: gradientStroke2,
                    borderColor: '#d346b1',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#d346b1',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#d346b1',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: chart_data,
                }]
            },
            options: gradientChartOptionsConfigurationWithTooltipPurple
        };
        let BigMainChart2 = new Chart(ctx2, config2);
        $("#02").click(function () {
            loadChart(BigMainChart2, links["top-day"], "dnld-big2")
            BigMainChart2.update();
        });

        $("#12").click(function () {
            loadChart(BigMainChart2, links["top-month"], "dnld-big2")
            BigMainChart2.update();
        });

        $("#22").click(function () {
            loadChart(BigMainChart2, links["top-year"], "dnld-big2")
            BigMainChart2.update();
        });


        var ctx2 = document.getElementById("chartBig3").getContext('2d');

        var gradientStroke2 = ctx2.createLinearGradient(0, 230, 0, 50);

        gradientStroke2.addColorStop(1, 'rgba(72,72,176,0.1)');
        gradientStroke2.addColorStop(0.4, 'rgba(72,72,176,0.0)');
        gradientStroke2.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors
        var config2 = {
            type: 'bar',
            data: {
                labels: chart_labels,
                datasets: [{
                    label: "My First dataset",
                    fill: true,
                    backgroundColor: gradientStroke2,
                    borderColor: '#d346b1',
                    borderWidth: 2,
                    borderDash: [],
                    borderDashOffset: 0.0,
                    pointBackgroundColor: '#d346b1',
                    pointBorderColor: 'rgba(255,255,255,0)',
                    pointHoverBackgroundColor: '#d346b1',
                    pointBorderWidth: 20,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 15,
                    pointRadius: 4,
                    data: chart_data,
                }]
            },
            options: gradientChartOptionsConfigurationWithTooltipPurple
        };
        let BigMainChart3 = new Chart(ctx2, config2);


        var ctx10 = document.getElementById("CountryChart1").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
        gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
        gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


        let chartSMCenterup = new Chart(ctx10, {
            type: 'bar',
            responsive: true,
            legend: {
                display: false
            },
            options: gradientBarChartConfiguration
        })

        // added charts

        var ctx10 = document.getElementById("CountryChart2").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(29,140,248,0.2)');
        gradientStroke.addColorStop(0.4, 'rgba(29,140,248,0.0)');
        gradientStroke.addColorStop(0, 'rgba(29,140,248,0)'); //blue colors


        let chartSMCenterdown = new Chart(ctx10, {
            type: 'bar',
            responsive: true,
            legend: {
                display: false
            },
            options: gradientBarChartConfiguration
        })

        var ctx = document.getElementById("md-chart-left").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
        gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

        var data = {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d048b6',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d048b6',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d048b6',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [80, 100, 70, 80, 120, 80],
            }]
        };

        var mdChartLeft = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipPurple
        });


        var ctx = document.getElementById("md-chart-right").getContext("2d");

        var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

        gradientStroke.addColorStop(1, 'rgba(72,72,176,0.2)');
        gradientStroke.addColorStop(0.2, 'rgba(72,72,176,0.0)');
        gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

        var data = {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
            datasets: [{
                label: "Data",
                fill: true,
                backgroundColor: gradientStroke,
                borderColor: '#d048b6',
                borderWidth: 2,
                borderDash: [],
                borderDashOffset: 0.0,
                pointBackgroundColor: '#d048b6',
                pointBorderColor: 'rgba(255,255,255,0)',
                pointHoverBackgroundColor: '#d048b6',
                pointBorderWidth: 20,
                pointHoverRadius: 4,
                pointHoverBorderWidth: 15,
                pointRadius: 4,
                data: [80, 100, 70, 80, 120, 80],
            }]
        };

        var mdChartRight = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: gradientChartOptionsConfigurationWithTooltipPurple
        });

        // added charts

        loadAllCharts(BigMainChart, BigMainChart2, chartSMCenterup, chartSMLeftup, chartSMRightup, chartSMLeftdown, chartSMCenterdown, chartSMRightdown, BigMainChart3, mdChartLeft, mdChartRight)

        // Big Chart2 date picker
        $(function () {
            $('input[name="big2-date"]').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD-MM-YYYY',
                }
            }, function (start, end, label) {
                console.log(start.format('YYYY-MM-DD'))
                loadChart(BigMainChart2, links["top-selling"], "dnld-big2", start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
            });
        });

        // status accept date picker
        $(function () {
            $('input[name="status-accept"]').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD-MM-YYYY',
                }
            }, function (start, end, label) {
                loadChart(chartSMLeftup, links["sale-status-a"], "dnld-slu", start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
            });
        });

        // status draft date picker
        $(function () {
            $('input[name="status-draft"]').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD-MM-YYYY',
                }
            }, function (start, end, label) {
                loadChart(chartSMCenterup, links["sale-status-d"], "dnld-scu", start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
            });
        });

        // status cancel date picker
        $(function () {
            $('input[name="status-cancel"]').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD-MM-YYYY',
                }
            }, function (start, end, label) {
                loadChart(chartSMRightup, links["sale-status-c"], "dnld-sru", start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
            });
        });

        // sales by employee date
        $(function () {
            $('input[name="sale-by-employee"]').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD-MM-YYYY',
                }
            }, function (start, end, label) {
                loadChart(mdChartRight, links["sales-by-employee"], "dnld-ddr", start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
            });
        });

        // sales by time of day date
        $(function () {
            $('input[name="sale-by-time-day"]').daterangepicker({
                opens: 'left',
                locale: {
                    format: 'DD-MM-YYYY',
                }
            }, function (start, end, label) {
                loadChart(mdChartLeft, links["sales-by-timeOf-day"], "dnld-ddl", start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'));
            });
        });
    },


    showNotification: function (from, align) {
        color = Math.floor((Math.random() * 4) + 1);

        $.notify({
            icon: "tim-icons icon-bell-55",
            message: "Welcome to <b>Black Dashboard</b> - a beautiful freebie for every web developer."

        }, {
            type: type[color],
            timer: 8000,
            placement: {
                from: from,
                align: align
            }
        });
    }

};


