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
var isPaused = false;
var takeProfitLineAdded = false;
var stopLossLineAdded = false;
var takeProfitValue;
var stopLossValue;
var buy = false;
var sell = false;
var userId;
var userIdFlag = false;
var closeTrade;
var start;
var stockType;
var amount;
var aiType;
var currentClose;
var uuid = generateUUID();


function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0,
            v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}


function createWebSocket() {
    if (socket === null || socket.readyState === WebSocket.CLOSED) {
        socket = new WebSocket('ws://localhost:8000/ws/ai-trade/?id=' + uuid);

        socket.onopen = function (e) {
            var urlParams = new URLSearchParams(window.location.search);
            start = urlParams.get('start');
            stockType = urlParams.get('stock_type');
            amount = urlParams.get('amount')
            aiType = urlParams.get('order_type')
            
            var dataToSend = {
                start: start,
                stockType: stockType,
                amount: amount,
                aiType: aiType,
            };
            $(document).ready(function() {
                var urlParams = new URLSearchParams(window.location.search);
                var amount = urlParams.get('amount');
            
                var thresholdValue = document.getElementById('money_in_account');
                if (parseFloat(amount) > parseFloat(thresholdValue.innerText.replace('£', ''))) {
                    $('#error-message').text('Amount willing to trade cannot exceed amount held in account. Please enter £'+ (amount - parseFloat(thresholdValue.innerText.replace('£', ''))).toFixed(2) +' less');
                    $("#error-modal").show();
        
                    $(".close").click(function() {
                        $("#error-modal").hide();
                    });
                }else {
                    // Sends the URL parameters to the consumer
                    socket.send(JSON.stringify(dataToSend));
                }
            });
            if (start === null || amount === null || stockType === null) {
                $('#error-message').text('Please enter values for Start, Amount and Stock Type');
                $("#error-modal").show();
    
                $(".close").click(function() {
                    $("#error-modal").hide();
                });
                socket.close()
            }
            console.log(dataToSend);
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


                if (djangoData.signal === 1 && !takeProfitLineAdded) {
                    closeTrade = graphData.data.datasets[0].data[graphData.data.datasets[0].data.length - 1]
                    takeProfitValue = currentClose + 4
                    stopLossValue = currentClose - 4
                    buy = true;
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













                if (takeProfitLineAdded) {
                    // Adds point to the take profit line on each run
                    var newGraphTakeLine = graphData.data.datasets[1].data;
                    newGraphTakeLine.push(takeProfitValue);
                    graphData.data.datasets[1].data = newGraphTakeLine;
                }
                if (stopLossLineAdded) {
                    // Adds point to the stop loss line on each run
                    var newGraphStopLine = graphData.data.datasets[2].data;
                    newGraphStopLine.push(stopLossValue);
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
                if (buy && djangoData.close > takeProfitValue) {
                    socket.send(JSON.stringify({'take_profit': takeProfitValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start, 'amount': amount}));
                    console.log(takeProfitValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                    userIdFlag = false;
                }
                else if (buy && djangoData.close < stopLossValue) {
                    socket.send(JSON.stringify({'stop_loss': stopLossValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start, 'amount': amount}));
                    console.log(stopLossValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                    userIdFlag = false;
                }
                else if (sell && djangoData.close < takeProfitValue) {
                    socket.send(JSON.stringify({'take_profit': takeProfitValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start, 'amount': amount}));
                    console.log(takeProfitValue)
                    console.log(userId)
                    console.log(closeTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    sell = false;
                    uaserIdFlag = false;
                }
                else if (sell && djangoData.close > stopLossValue) {
                    socket.send(JSON.stringify({'stop_loss': stopLossValue, 'user_id': userId, 'close_trade': closeTrade, 'stockType': stockType, 'start': start, 'amount': amount}));
                    console.log(stopLossValue)
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
                    stockType: stockType,
                    amount: amount,
                    aiType: aiType,
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
            stockType: stockType,
        };

        console.log(dataToSend);
        socket.send(JSON.stringify(dataToSend));
    }
    isPaused = false;
});

document.getElementById('stop').addEventListener('click', function () {
    isPaused = !isPaused; // Toggle the paused state
});

$(document).ready(function() {
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
            userId = data["user_id"]
            }
        });
    })
});
