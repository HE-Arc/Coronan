var now = new Date();
var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
var tmp = new Date(today);
var lastSunday = new Date(tmp.setDate(today.getDate() - today.getDay()));
var week = [];

for (i = 0; i < 7; i++) {
  lastSunday = new Date(lastSunday.getFullYear(), lastSunday.getMonth(), lastSunday.getDate() + 1)
  week.push(lastSunday.getFullYear() + "/" + lastSunday.getMonth() + "/" + lastSunday.getDate());
}
console.log(week);


var cases = [];
var dates = [];
$.getJSON('https://corona-api.com/countries/ch', function (data) {
  var timeline = data.data.timeline;

  console.log(today.getDay());
  n = today.getDay();
  if (n == 0) n = 7;

  timeline.slice(0, n).reverse().forEach(function (data) {
    cases.push(data.new_confirmed);
    dates.push(data.date);
  });

  const cumulativeSum = (sum => value => sum += value)(0);
  cases = cases.map(cumulativeSum);

  while (cases.length < 7)
    cases.push(null);
  console.log(cases);


  var ctx = document.getElementById('myChart').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: week,
      datasets: [{
        spanGaps: true,
        label: 'Cases confirmed',
        backgroundColor: 'rgb(156, 99, 156)',
        borderColor: 'rgb(156, 99, 156)',
        data: cases,
      }]
    },
  });

});