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
var user_id=1;
function bid_offer_handler(){
  this.bid_price = 0;
  this.set_bid_price = function (bid_price){
    if(bid_price!==this.bid_price){
      this.bid_price = bid_price;
      this.values_updated = true;
    }
  };
  this.bid_quantity = 0;
  this.set_bid_quantity = function (bid_quantity){
    if(bid_quantity!==this.bid_quantity){
      this.bid_quantity = bid_quantity;
      this.values_updated = true;
    }
  };
  this.offer_price = 0;
  this.set_offer_price = function (offer_price){
    if(offer_price!==this.offer_price){
      this.offer_price = offer_price;
      this.values_updated = true;
    }
  };
  this.offer_quantity = 0;
  this.set_offer_quantity = function (offer_quantity){
    if(offer_quantity!==this.offer_quantity){
      this.offer_quantity = offer_quantity;
      this.values_updated = true;
    }
  };
  this.update_ui_quantities = function(){
    document.getElementById("current_offer_price").innerHTML = "£" + this.offer_price;
    document.getElementById("current_offer_quantity").innerHTML = this.offer_quantity;
    document.getElementById("current_bid_price").innerHTML = "£" + this.bid_price;
    document.getElementById("current_bid_quantity").innerHTML = this.bid_quantity;
  };
  this.reset_form = function(){
    var form = document.getElementById("bid_form");
    // For each of the boxes update to what we have stored here
    form.elements["offer_price"].value = 0;
    form.elements["offer_quantity"].value = 0;
    form.elements["bid_price"].value = 0;
    form.elements["bid_quantity"].value = 0;
  };
  this.gather_ui_quantities = function(){
    var form = document.getElementById("bid_form");
    // For each of the boxes update to what we have stored here
    this.offer_price = form.elements["offer_price"].value;
    this.offer_quantity = form.elements["offer_quantity"].value;
    this.bid_price = form.elements["bid_price"].value;
    this.bid_quantity = form.elements["bid_quantity"].value;
    this.reset_form();
  };
}

function update_orders_from_ui(){
  orders.gather_ui_quantities();
  update_position();
};

function User(){
  this.id = 1;
  this.cash=100;
  this.holding=0;
  this.update_ui_quantities = function(){
    var cash = document.getElementById("cash_value");
    cash.value = this.cash;
    var holding = document.getElementById("holding_value");
    holding.value = this.holding;
  };
}

var orders = new bid_offer_handler();
var user = new User();

function on_successful_update_request(result){ // Has to be there !
  //Add the data to the graph
  var user_data = result.user_data;
  var price_data = result.price_data;
  update_user_offers(user_data);
  update_user(user_data);
  update_price_history(price_data);
}

function update_user_offers(user_data){
  //need to update the values from bid_offer_handler
  //validate that result has the values needed.
  orders.bid_price = user_data.bid.price;
  orders.bid_quantity = user_data.bid.quantity;
  orders.offer_price = user_data.offer.price;
  orders.offer_quantity = user_data.offer.quantity;
  orders.update_ui_quantities();
}
function update_user(user_data){
  user.cash = user_data.cash;
  user.holding = user_data.holding;
  user.update_ui_quantities();
}
function update_price_history(price_data){
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
      price_data.forEach(function(data){
        dataset.data.push(data);
      });
    });

    window.myLine.update();
  }
}

function request_update(data, success, failure){
  $.ajax({
    url : "/update", //PHP file to execute
    dataType: "json",
    type: "post",
    contentType: "application/json",
    // could probably do with only sending the extra information when there is a change
    data: data,
    success: success,
    error : failure
  });
}

function update_position(){
  var data = JSON.stringify({
    user_id : user_id, 
    bid:{price: orders.bid_price, quantity: orders.bid_quantity},
    offer:{price: orders.offer_price, quantity: orders.offer_quantity}}); // Parameters passed to the server

  request_update(data, on_successful_update_request, function(result, statut, error){});
}

function main_loop(){
  var data = JSON.stringify({user_id : user_id});
  request_update(data, on_successful_update_request, function(result, statut, error){});
}



window.onload = function() {
  var ctx = document.getElementById('canvas').getContext('2d');
  window.myLine = new Chart(ctx, config);
  window.setInterval(main_loop, 1000);
};


var colorNames = Object.keys(window.chartColors);
