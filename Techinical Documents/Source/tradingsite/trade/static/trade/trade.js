const ctx = document.getElementById('myChart');

var graphData = {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Price of stock',
        data: [],
        borderWidth: 1
      }]
    },
    options: {}
}

var myChart = new Chart(ctx, graphData);


var socket = null;
var isPaused = false; // Variable to track whether graph updates are paused
var takeProfitLineAdded = false;
var stopLossLineAdded = false;
var takeProfitValue;
var stopLossValue;
var buy = false;
var sell = false;

function createWebSocket() {
    if (socket === null || socket.readyState === WebSocket.CLOSED) {
        socket = new WebSocket('ws://localhost:8000/ws/trade/');

        socket.onopen = function () {
            var urlParams = new URLSearchParams(window.location.search);
            var start = urlParams.get('start');
            var stockType = urlParams.get('stock_type');
            
            var dataToSend = {
                start: start,
                stockType: stockType
            };
            console.log(dataToSend);
            socket.send(JSON.stringify(dataToSend));
        };
        
        socket.onmessage = function (e) {
            if (!isPaused) { // Check if updates are paused
                var djangoData = JSON.parse(e.data);
                console.log(djangoData);

                var newGraphDataValue = graphData.data.datasets[0].data;
                var newGraphDataDate = graphData.data.labels;

                if (newGraphDataDate.length > 36) {
                    newGraphDataValue.shift();
                    newGraphDataDate.shift();
                }

                newGraphDataValue.push(djangoData.open);
                newGraphDataDate.push(djangoData.date);
               
                graphData.data.datasets[0].data = newGraphDataValue;
                graphData.data.labels = newGraphDataDate

                if (takeProfitLineAdded) {
                    socket.send(JSON.stringify({'open': djangoData.open}));// Only need one of these
                    console.log(djangoData.open)
                    var newGraphTakeLine = graphData.data.datasets[1].data;
                    console.log(takeProfitValue)
                    newGraphTakeLine.push(takeProfitValue);
                    graphData.data.datasets[1].data = newGraphTakeLine;
                }
                if (stopLossLineAdded) {
                    var newGraphStopLine = graphData.data.datasets[2].data;
                    console.log(stopLossValue)
                    newGraphStopLine.push(stopLossValue);
                    graphData.data.datasets[2].data = newGraphStopLine;
                }
                if (buy && djangoData.open > takeProfitValue) {
                    socket.send(JSON.stringify({'take_profit': takeProfitValue}));
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                }
                else if (buy && djangoData.open < stopLossValue) {
                    socket.send(JSON.stringify({'stop_loss': stopLossValue}));
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                }
                if (sell && djangoData.open < takeProfitValue) {
                    socket.send(JSON.stringify({'take_profit': takeProfitValue}));
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    sell = false;
                }
                else if (sell && djangoData.open > stopLossValue) {
                    socket.send(JSON.stringify({'stop_loss': stopLossValue}));
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    sell = false;
                }
                myChart.update('none');
            }
        }
    }
}

// Event listener for the button to create WebSocket connection
document.getElementById('confirm').addEventListener('click', function () {
    createWebSocket();
    isPaused = false;
});

// Event listener for the button to pause graph updates
document.getElementById('stop').addEventListener('click', function () {
    isPaused = !isPaused; // Toggle the paused state
});

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
            // Draw a straight line at take_profit value
            takeProfitValue = parseFloat(data["take_profit"])
            stopLossValue = parseFloat(data["stop_loss"])
            if (data["order_type"] === 'buy' && takeProfitValue <= stopLossValue) {

                $("#result").text('no buy');
            }
            else if (data["order_type"] === 'sell' && takeProfitValue >= stopLossValue) {
                $("#result").text('no sell');
            }
            else if (data["order_type"] === 'buy' && takeProfitValue >= stopLossValue) {
                buy = true;
                var takeProfitLineData = Array(myChart.data.labels.length).fill(takeProfitValue);
                var stopLossLineData = Array(myChart.data.labels.length).fill(stopLossValue);
                
                // Add the straight line data to the datasets
                myChart.data.datasets.push({
                    label: 'Take Profit',
                    data: takeProfitLineData,
                    borderColor: 'green',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0
                });
                // Add the straight line data to the datasets
                myChart.data.datasets.push({
                    label: 'Stop Loss',
                    data: stopLossLineData,
                    borderColor: 'red',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0
                });
                takeProfitLineAdded = true;
                stopLossLineAdded = true;
                
                myChart.update('none');
            }
            else if (data["order_type"] === 'sell' && takeProfitValue <= stopLossValue) {
                sell = true;
                var takeProfitLineData = Array(myChart.data.labels.length).fill(takeProfitValue);
                var stopLossLineData = Array(myChart.data.labels.length).fill(stopLossValue);
                
                // Add the straight line data to the datasets
                myChart.data.datasets.push({
                    label: 'Take Profit',
                    data: takeProfitLineData,
                    borderColor: 'green',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0
                });
                // Add the straight line data to the datasets
                myChart.data.datasets.push({
                    label: 'Stop Loss',
                    data: stopLossLineData,
                    borderColor: 'red',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0
                });
                takeProfitLineAdded = true;
                stopLossLineAdded = true;
                
                myChart.update('none');
                }
            }
        });
    })
);