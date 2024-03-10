const ctx = document.getElementById('Chart');

var colors = [
    'rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 206, 86, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)'
]

var allLabels = ['Rent', 'Bills', 'Food', 'Invest', 'Savings', 'Luxury']


// AJAX
$(document).ready(
    $('#post-form').submit(function(e){
        e.preventDefault();
        var serializedData = $(this).serialize();

        $.ajax({
        type:"POST",
        url: "",
        data:  serializedData,
        success: function(data){
            var allData = [
                data.rent,
                data.bills,
                data.food,
                data.invest,
                data.savings,
                data.luxury, 
            ]
            maximum = data.rent+data.bills+data.food+data.invest+data.savings+data.luxury
            
            if (data.total >= maximum) {
                if (data.choices === "Pie") {
                    const ctx = document.getElementById('Chart');
                    var graphData = {
                        type: 'pie',
                        data: {
                            labels: allLabels,
                            datasets: [{
                                data: allData,
                                backgroundColor: colors,
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false
                        }
                    };
                    var myChart = new Chart(ctx, graphData);
                } else if (data.choices === "Bar") {
                    const ctx = document.getElementById('Chart');
                    var graphData = {
                        type: 'bar',
                        data: {
                            labels: allLabels,
                            datasets: [{
                                label: 'Expenses',
                                data: allData,
                                backgroundColor: colors,
                                borderColor: 'rgba(0, 0, 0, 0.2)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    };
                    var myChart = new Chart(ctx, graphData);
                } else if (data.choices === "Polar") {
                    const ctx = document.getElementById('Chart');
                    var graphData = {
                        type: 'polarArea',
                        data: {
                            datasets: [{
                                data: allData,
                                backgroundColor: colors,
                                borderColor: 'rgba(0, 0, 0, 0.2)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                r: {
                                    beginAtZero: true
                                }
                            }
                        }
                    };
                    var myChart = new Chart(ctx, graphData);
                } else if (data.choices === "Radar") {
                    const ctx = document.getElementById('Chart');
                    var graphData = {
                        type: 'radar',
                        data: {
                            labels: allLabels,
                            datasets: [{
                                label: 'Expenses',
                                data: allData,
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                r: {
                                    min: 0,
                                    max: 100, // You can adjust the maximum value as needed
                                    stepSize: 20 // You can adjust the step size as needed
                                }
                            }
                        }
                    };
                    var myChart = new Chart(ctx, graphData);
                }
            } else { return null }
        }
        });
    })
);