document.addEventListener('DOMContentLoaded', function() {
    // Get data from Flask template variables
    var ratingsDistributionData = ratingsData;
    var ratingsVsRevenueData = RevenueData;
    var votesVsRatingsData = votes;

    // IMDb Ratings Distribution Chart (Chart.js)
    var ratingsDistributionCtx = document.getElementById('ratingsDistributionChart').getContext('2d');
    new Chart(ratingsDistributionCtx, {
        type: 'bar',
        data: {
            labels: ratingsDistributionData.map(entry => entry.IMDB_Rating),
            datasets: [{
                label: 'Number of Movies',
                data: ratingsDistributionData.map(entry => entry.Count),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // IMDb Ratings vs. Gross Revenue Chart (Plotly)
    var ratingsVsRevenueDiv = document.getElementById('imdb-ratings-vs-gross-revenue-chart');
    var ratingsVsRevenueTrace = {
        x: ratingsVsRevenueData.map(entry => entry.IMDB_Rating),
        y: ratingsVsRevenueData.map(entry => entry.Gross),
        mode: 'markers',
        type: 'scatter',
        marker: {color: 'rgba(255, 99, 132, 0.5)'},
        text: 'IMDb Ratings vs. Gross Revenue'
    };
    var ratingsVsRevenueLayout = {
        xaxis: {title: 'IMDb Rating'},
        yaxis: {title: 'Gross Revenue'}
    };
    Plotly.newPlot(ratingsVsRevenueDiv, [ratingsVsRevenueTrace], ratingsVsRevenueLayout);

    // Votes vs. Ratings Chart (D3.js)
    var votesVsRatingsSvg = d3.select('#votes-vs-ratings-chart');
    var margin = {top: 20, right: 20, bottom: 30, left: 50};
    var width = +votesVsRatingsSvg.attr('width') - margin.left - margin.right;
    var height = +votesVsRatingsSvg.attr('height') - margin.top - margin.bottom;

    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    var votesVsRatingsLine = d3.line()
        .x(function(d) { return x(d.IMDB_Rating); })
        .y(function(d) { return y(d.No_of_Votes); });

    var g = votesVsRatingsSvg.append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    x.domain(d3.extent(votesVsRatingsData, function(d) { return d.IMDB_Rating; }));
    y.domain(d3.extent(votesVsRatingsData, function(d) { return d.No_of_Votes; }));

    g.append('path')
        .datum(votesVsRatingsData)
        .attr('fill', 'none')
        .attr('stroke', 'rgba(54, 162, 235, 1)')
        .attr('stroke-linejoin', 'round')
        .attr('stroke-linecap', 'round')
        .attr('stroke-width', 1.5)
        .attr('d', votesVsRatingsLine);

    g.append('g')
        .attr('transform', 'translate(0,' + height + ')')
        .call(d3.axisBottom(x));

    g.append('g')
        .call(d3.axisLeft(y));

});
