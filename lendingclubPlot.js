// LendingClub default visualization
// Matt Shadish
// 2/4/2018



var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// define the SVG elements first
var svg = d3.select("body").attr("align", "center").append("svg")
			.attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom);



// define the form of the output date
var parseDate = d3.timeParse("%Y-%m-%d");

// x, y, and z variables
var x = d3.scaleTime().range([0, width]),
    y = d3.scaleLinear().range([height, 0]),
    z = d3.scaleOrdinal(d3.schemeCategory10);

// initialize d3 stacking
var stack = d3.stack();

var area = d3.area()
    .x(function(d, i) { return x(d.data.date); })
    .y0(function(d) { return y(d[0]); })
    .y1(function(d) { return y(d[1]); });

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


//
// PLOT TEXT HERE
//
// add text for the x- and y-axes                                                                                          
svg.append('text')
    .attr('x', width/2)
    .attr('y', height + margin.top + margin.bottom)
    .style('text-anchor', 'middle')
    .style('font-size', 20)
    .text('Date');

// y-axis, which is the percentage rate of loans                                                                                                  
svg.append('text')
    .attr('x', margin.left * 2)
    .attr('y', margin.top)
    .style('text-anchor', 'middle')
    .style('font-size', 20)
    .text('% of Notes');

// Title here                                                                                                          
svg.append('text')
	.attr('x', (margin.left + width)/2)
	.attr('y', margin.top)
	.style('text-anchor', 'middle')
	.style('font-size', 24)
	.text('Troubled LendingClub Loans over Time');


// Read in CSV data
d3.csv("data.csv", type, function(error, data) {
  if (error) throw error;

  // use this to read the 
  var keys = data.columns.slice(1);

  x.domain(Array( parseDate("2016-10-01"), d3.extent(data, function(d) { return d.date; })[1] ));
  y.domain([0, d3.max(data, function(d) {
	  	return keys.reduce( function(sum, key) {
	  		return sum + d[key]; 
	  	}, 0); 
	  // add 5% to the y-axis to show some relativity
	  }) + 0.05
  ]);
  console.log(y.domain());
  z.domain(keys);
  stack.keys(keys);
  

  var layer = g.selectAll(".layer")
    .data(stack(data
		.filter(function(y) { return y.date > parseDate("2016-10-01") })))
    .enter().append("g")
    .attr("class", "layer");

  layer.append("path")
      .attr("class", "area")
      .style("fill", function(d) { return z(d.key); })
      .attr("d", area);

  layer
  	// take out the filter
  	//.filter(function(d) { return d[d.length - 1][1] - d[d.length - 1][0] > 0.01; })
    .append("text")
      .attr("x", width - 6)
      .attr("y", function(d) { return y((d[d.length - 1][0] + d[d.length - 1][1]) / 2); })
      .attr("dy", ".35em")
      .style("font", "15px sans-serif")
      .style("text-anchor", "end")
      .style('font-weight', 900)
      .text(function(d) { return d.key; });

  g.append("g")
      .attr("class", "axis axis--x")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

  g.append("g")
      .attr("class", "axis axis--y")
      .call(d3.axisLeft(y).ticks(10, "%"));
});

function type(d, i, columns) {
  d.date = parseDate(d.date);
  // convert to a number
  for (var i = 1, n = columns.length; i < n; ++i) d[columns[i]] = +d[columns[i]];
  return d;
}
