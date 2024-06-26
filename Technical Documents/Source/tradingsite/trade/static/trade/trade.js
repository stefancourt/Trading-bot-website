const ctx = document.getElementById('myChart');

// Empty chart
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
var isPaused = false;
var takeProfitLineAdded = false;
var stopLossLineAdded = false;
var takeProfitValue;
var takeProfitAcceptedValue;
var stopLossValue;
var stopLossAcceptedValue;
var buy = false;
var sell = false;
var userId;
var userIdFlag = false;
var closeTrade;
var start;
var stockType;
var currentClose;
var amount;
var amountExceded;

function createWebSocket() {
    if (socket === null || socket.readyState === WebSocket.CLOSED) {
        socket = new WebSocket('ws://localhost:8000/ws/trade/');

        socket.onopen = function () {
            var urlParams = new URLSearchParams(window.location.search);
            start = urlParams.get('start');
            stockType = urlParams.get('stock_type');
            
            var dataToSend = {
                start: start,
                stockType: stockType
            };
            if (start === null || stockType === null) {
                $('#error-message').text('Please enter values for Start and Stock Type');
                $("#error-modal").show();
    
                $(".close").click(function() {
                    $("#error-modal").hide();
                });
                socket.close()
            }
            console.log(dataToSend);
            // Sends the URL parameters to the consumer
            socket.send(JSON.stringify(dataToSend));
        };
        
        socket.onmessage = function (e) {
            if (!isPaused) { // Check if updates are paused
                var djangoData = JSON.parse(e.data);
                console.log(djangoData);

                // Changes the user's balance on the web page without needing to refreshing the page
                if (djangoData.money_in_account) {
                    var moneyInAccountElement = document.getElementById('money_in_account');
                    if (moneyInAccountElement) {
                        moneyInAccountElement.innerText = "£" + djangoData.money_in_account.toFixed(2);
                    }
                }
                if (djangoData.first_date !== undefined) {
                    $('#error-message').text('Please enter a valid start date that starts after '+djangoData.first_date);
                    $("#error-modal").show();
        
                    $(".close").click(function() {
                        $("#error-modal").hide();
                    });
                    // Closes socket if the date entered is invalid
                    socket.close()
                }
                if (djangoData.last_date !== undefined) {
                    $('#error-message').text('Last date of stock has been reached please input another date to start from before '+djangoData.last_date);
                    $("#error-modal").show();
        
                    $(".close").click(function() {
                        $("#error-modal").hide();
                    });
                    // Closes socket if the date entered is invalid
                    socket.close()
                }
                currentClose = djangoData.close

                var newGraphDataValue = graphData.data.datasets[0].data;
                var newGraphDataDate = graphData.data.labels;

                if (newGraphDataDate.length > 36) {
                    newGraphDataValue.shift();
                    newGraphDataDate.shift();
                }

                // Adds close point of stock for the date to the graph
                newGraphDataValue.push(djangoData.close);
                newGraphDataDate.push(djangoData.date);
               
                graphData.data.datasets[0].data = newGraphDataValue;
                graphData.data.labels = newGraphDataDate

                if (takeProfitLineAdded) {
                    var newGraphTakeLine = graphData.data.datasets[1].data;
                    // Adds point to the take profit line on each run
                    newGraphTakeLine.push(takeProfitAcceptedValue);
                    graphData.data.datasets[1].data = newGraphTakeLine;
                }
                if (stopLossLineAdded) {
                    var newGraphStopLine = graphData.data.datasets[2].data;
                    // Adds point to the stop loss line on each run
                    newGraphStopLine.push(stopLossAcceptedValue);
                    graphData.data.datasets[2].data = newGraphStopLine;
                }
                // Sets the date one day forward
                start = new Date(djangoData.date);
                start.setDate(start.getDate() + 1);

                // Format the date back to "YYYY-MM-DD" format
                var year = start.getFullYear();
                var month = (start.getMonth() + 1).toString().padStart(2, '0'); // Month is zero-based
                var day = start.getDate().toString().padStart(2, '0');

                start = year + '-' + month + '-' + day;

                // If take-profit/stop-loss hit sends the value to the consumer
                if (buy && djangoData.close > takeProfitAcceptedValue) {
                    socket.send(JSON.stringify({'amount': amount, 'take_profit': takeProfitAcceptedValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start}));
                    console.log(takeProfitAcceptedValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                    userIdFlag = false;
                }
                else if (buy && djangoData.close < stopLossAcceptedValue) {
                    socket.send(JSON.stringify({'amount': amount, 'stop_loss': stopLossAcceptedValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start}));
                    console.log(stopLossAcceptedValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                    userIdFlag = false;
                }
                else if (sell && djangoData.close < takeProfitAcceptedValue) {
                    socket.send(JSON.stringify({'amount': amount, 'take_profit': takeProfitAcceptedValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType,'start': start}));
                    console.log(takeProfitAcceptedValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    sell = false;
                    uaserIdFlag = false;
                }
                else if (sell && djangoData.close > stopLossAcceptedValue) {
                    socket.send(JSON.stringify({'amount': amount, 'stop_loss': stopLossAcceptedValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start}));
                    console.log(stopLossAcceptedValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    sell = false;
                    userIdFlag = false;
                }
                else {
                    console.log(start);
                    var dataToSend = {
                    start: start,
                    stockType: stockType
                };
                console.log(dataToSend);
                socket.send(JSON.stringify(dataToSend));
                }
                // Points are animated from 0 axis which looks clunky so no aninmations
                myChart.update('none');
            }
        }
    }
}
// Event listener for the button to create WebSocket connection
document.getElementById('confirm').addEventListener('click', function () {
    createWebSocket();
    if (isPaused) {
        var dataToSend = {
            start: start,
            stockType: stockType
        };

        console.log(dataToSend);
        socket.send(JSON.stringify(dataToSend));
    }
    isPaused = false;
});

// Event listener for the button to pause graph updates
document.getElementById('stop').addEventListener('click', function () {
    isPaused = !isPaused; // Toggle the paused state
});

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

        // Ajax for hendling POST request
        $.ajax({
        type:"POST",
        url: "",
        data:  serializedData,
        success: function(data){
            // Draw a straight line at take_profit value
            amount = data["amount"]
            userId = data["user_id"]
            userIdFlag = true;
            closeTrade = graphData.data.datasets[0].data[graphData.data.datasets[0].data.length - 1]
            takeProfitValue = parseFloat(data["take_profit"])
            stopLossValue = parseFloat(data["stop_loss"])
            var thresholdValue = document.getElementById('money_in_account');
            if (parseFloat(amount) <= parseFloat(thresholdValue.innerText.replace('£', ''))) {
                amountExceded = false
            }
            else if (parseFloat(amount) > parseFloat(thresholdValue.innerText.replace('£', ''))) {
                $('#error-message').text('Amount willing to trade cannot exceed amount held in account. Please enter £'+ (amount - parseFloat(thresholdValue.innerText.replace('£', ''))).toFixed(2) +' less');
                $("#error-modal").show();
                amountExceded = true
            }
            if (buy) {
                $('#error-message').text('Cannot place another trade while one is still active');
                $('#error-modal').show();
            }
            else if (sell) {
                $('#error-message').text('Cannot place another trade while one is still active');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'buy' && takeProfitValue <= stopLossValue) {
                $('#error-message').text('The value of your Stop Loss cannot be greater than your Take Profit on a buy order');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'buy' && takeProfitValue <= currentClose) {
                $('#error-message').text('You cannot place a buy order where the Take Proft value is below the current price of the stock');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'buy' && stopLossValue >= currentClose) {
                $('#error-message').text('You cannot place a buy order where the Stop Loss value is above the current price of the stock');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'buy' && takeProfitValue <= stopLossValue) {
                $('#error-message').text('The value of your Take Profit cannot be greater than your Stop Loss on a buy order');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'sell' && takeProfitValue >= currentClose) {
                $('#error-message').text('You cannot place a sell order where the Take Profit value is above the current price of the stock');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'sell' && stopLossValue <= currentClose) {
                $('#error-message').text('You cannot place a sell order where the Stop Loss value is below the current price of the stock');
                $('#error-modal').show();
            }
            else if (data["order_type"] === 'buy' && takeProfitValue >= stopLossValue && amountExceded === false) {
                buy = true;
                takeProfitAcceptedValue = takeProfitValue
                stopLossAcceptedValue = stopLossValue
                var takeProfitLineData = Array(myChart.data.labels.length).fill(takeProfitValue);
                var stopLossLineData = Array(myChart.data.labels.length).fill(stopLossValue);
                
                // Add the Take Profit line data to the datasets
                myChart.data.datasets.push({
                    label: 'Take Profit',
                    data: takeProfitLineData,
                    borderColor: 'green',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0
                });
                // Add the Stop Loss line data to the datasets
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
            else if (data["order_type"] === 'sell' && takeProfitValue <= stopLossValue && amountExceded === false) {
                sell = true;
                takeProfitAcceptedValue = takeProfitValue
                stopLossAcceptedValue = stopLossValue
                var takeProfitLineData = Array(myChart.data.labels.length).fill(takeProfitValue);
                var stopLossLineData = Array(myChart.data.labels.length).fill(stopLossValue);
                
                // Add the Take Profit line data to the datasets
                myChart.data.datasets.push({
                    label: 'Take Profit',
                    data: takeProfitLineData,
                    borderColor: 'green',
                    borderWidth: 1,
                    fill: false,
                    pointRadius: 0
                });
                // Add the Stop Loss line data to the datasets
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
});