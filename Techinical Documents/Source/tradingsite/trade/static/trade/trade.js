const ctx = document.getElementById('myChart');

var graphData = {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: '# of Votes',
        data: [],
        borderWidth: 1
      }]
    },
    options: {}
}

  
var myChart = new Chart(ctx, graphData);

var socket = null;
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

            myChart.update();
        }
    }
}

// Event listener for the button
document.getElementById('confirm').addEventListener('click', function () {
    createWebSocket();
});