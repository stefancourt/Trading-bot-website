var colors = [
    'rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 206, 86, 0.8)',
    'rgba(75, 192, 192, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)'
]

var allLabels = ['Rent', 'Bills', 'Food', 'Invest', 'Savings', 'Luxury']


$(document).ready(function() {
    $('.close').click(function() {
        $('#error-modal').hide();
    });

    $(window).click(function(event) {
        if (event.target.id == 'error-modal') {
            $('#error-modal').hide();
        }
    });

    $('#post-form').submit(function(e){
        e.preventDefault();
        var serializedData = $(this).serialize();

        // AJAX handling POST request
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
            var maxData = Math.max(...allData);
            if (data.total >= maximum) {
                const ctx = document.getElementById('Chart');
                // Checks if there is already a graph present
                if (window.myChart instanceof Chart) {
                    // Removes graph from the page
                    window.myChart.destroy();
                }
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
                } else if (data.choices === "Polar") {
                    const ctx = document.getElementById('Chart');
                    var graphData = {
                        type: 'polarArea',
                        data: {
                            labels: allLabels,
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
                                    max: Math.ceil(maxData / 100) * 100,
                                    stepSize: 20
                                }
                            }
                        }
                    };
                }
                // Creates a graph
                window.myChart = new Chart(ctx, graphData);
            } else {
                $('#error-message').text('Combined total of spendatures must not exceed the total balance. Please enter £'+ (maximum - data.total).toFixed(2) +' less');
                $('#error-modal').show();
            }
        }
        });
    })
});