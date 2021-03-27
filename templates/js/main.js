window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};

var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var config = {
    type: 'line',
    data: {
        labels: MONTHS,
        datasets: [{
            label: 'My First dataset',
            backgroundColor: window.chartColors.red,
            borderColor: window.chartColors.red,
            data: [1,2,3,4,5,6,7,8,3,5,6,7],
            fill: false,
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Chart.js Line Chart'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Month'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
};

//add event loop to poll every second for data.
user_id=1;
window.onload = function() {
  var ctx = document.getElementById('canvas').getContext('2d');
  window.myLine = new Chart(ctx, config);
  window.setInterval(function(){
    $.ajax({
       url : '/update', //PHP file to execute
       dataType: 'json',
       type: 'post',
       contentType: 'application/json',
       data: JSON.stringify({user_id : user_id}), // Parameters passed to the server
       success : function(result){ // Has to be there !
          //Add the data to the graph
              if (config.data.datasets.length > 0) {
                  var month = MONTHS[config.data.labels.length % MONTHS.length];
                  config.data.labels.push(month);
                  config.data.datasets.forEach(function(dataset) {
                  // source https://stackoverflow.com/a/62519003/1320619
                      if (dataset.data.length > 20) {
                        // Remove the oldest data and label
                        dataset.data.shift();
                        config.data.labels.shift();
                      }
                      result.price_data.forEach(function(data){
                        dataset.data.push(data);
                      })
                  });

                  window.myLine.update();
              }
       },
       error : function(result, statut, error){ // Handle errors

       }
    });
  }, 1000);
};


var colorNames = Object.keys(window.chartColors);
