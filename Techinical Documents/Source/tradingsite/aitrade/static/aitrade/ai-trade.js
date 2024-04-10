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
var userId;
var userIdFlag = false;
var openTrade;
var start;
var stockType;
var currentOpen;
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
        socket = new WebSocket('ws://localhost:8000/ws/ai-trade/');

        socket.onopen = function (e) {
            var urlParams = new URLSearchParams(window.location.search);
            start = urlParams.get('start');
            stockType = urlParams.get('stock_type');
            
            var dataToSend = {
                start: start,
                stockType: stockType,
                uuid: uuid
            };
            console.log(dataToSend);
            socket.send(JSON.stringify(dataToSend));
        };
        
        socket.onmessage = function (e) {
            if (!isPaused) { // Check if updates are paused
                var djangoData = JSON.parse(e.data);
                console.log(djangoData);

                if (djangoData.money_in_account) {
                    var moneyInAccountElement = document.getElementById('money_in_account');
                    if (moneyInAccountElement) {
                        moneyInAccountElement.innerText = "£" + djangoData.money_in_account.toFixed(2);
                    }
                }

                currentOpen = djangoData.open

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
                    var newGraphTakeLine = graphData.data.datasets[1].data;
                    newGraphTakeLine.push(takeProfitValue);
                    graphData.data.datasets[1].data = newGraphTakeLine;
                }
                if (stopLossLineAdded) {
                    var newGraphStopLine = graphData.data.datasets[2].data;
                    newGraphStopLine.push(stopLossValue);
                    graphData.data.datasets[2].data = newGraphStopLine;
                }
                start = new Date(djangoData.date);
                start.setDate(start.getDate() + 1);

                // Format the date back to "YYYY-MM-DD" format
                var year = start.getFullYear();
                var month = (start.getMonth() + 1).toString().padStart(2, '0'); // Month is zero-based
                var day = start.getDate().toString().padStart(2, '0');

                start = year + '-' + month + '-' + day;
                if (buy && djangoData.open > takeProfitValue) {
                    socket.send(JSON.stringify({'take_profit': takeProfitValue, 'user_id': userId, 'open_trade': openTrade, 'stockType': stockType, 'start': start, 'uuid': uuid}));
                    console.log(takeProfitValue)
                    console.log(userId)
                    console.log(openTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                    userIdFlag = false;
                }
                else if (buy && djangoData.open < stopLossValue) {
                    socket.send(JSON.stringify({'stop_loss': stopLossValue, 'user_id': userId, 'open_trade': openTrade, 'stockType': stockType, 'start': start, 'uuid': uuid}));
                    console.log(stopLossValue)
                    console.log(userId)
                    console.log(openTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    buy = false;
                    userIdFlag = false;
                }
                else if (sell && djangoData.open < takeProfitValue) {
                    socket.send(JSON.stringify({'take_profit': takeProfitValue, 'user_id': userId, 'open_trade': openTrade, 'stockType': stockType, 'start': start, 'uuid': uuid}));
                    console.log(takeProfitValue)
                    console.log(userId)
                    console.log(openTrade)
                    graphData.data.datasets.splice(1, 1)
                    graphData.data.datasets.splice(1, 1)
                    takeProfitLineAdded = null;
                    stopLossLineAdded = null;
                    sell = false;
                    uaserIdFlag = false;
                }
                else if (sell && djangoData.open > stopLossValue) {
                    socket.send(JSON.stringify({'stop_loss': stopLossValue, 'user_id': userId, 'open_trade': openTrade, 'stockType': stockType, 'start': start, 'uuid': uuid}));
                    console.log(stopLossValue)
                    console.log(userId)
                    console.log(openTrade)
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
                    uuid: uuid
                };
                console.log(dataToSend);
                socket.send(JSON.stringify(dataToSend));
                }
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
