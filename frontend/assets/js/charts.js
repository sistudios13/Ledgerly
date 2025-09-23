// CHART 1
var options = {
	series: [
		{
			name: "Account Balance",
			data: rawData,
			parsing: {
				x: "date",
				y: "value",
			},
		},
	],
	chart: {
		type: "area",
		height: 400,
		zoom: {
			enabled: false,
		},
		toolbar: {
			tools: {
				download: false,
			},
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "smooth",
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return "$" + val.toFixed(2);
			},
		},
	},

	labels: [],
	xaxis: {
		type: "datetime",
	},
	yaxis: {
		opposite: true,

		labels: {
			formatter: function (val) {
				return "$" + val.toFixed(2);
			},
		},
	},
};
var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();

// CHART 2

var options2 = {
	series: [],

	chart: {
		height: 400,
		type: "pie",
	},

	theme: {
		monochrome: {
			enabled: true,
		},
	},
	legend: {
		show: false,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return "$" + val.toFixed(2);
			},
		},
	},
	dataLabels: {
		enabled: false,
	},
	responsive: [
		{
			breakpoint: 480,
			options: {
				chart: {
					width: "100%",
					height: "100%",
				},
			},
		},
	],
};

var chart2 = new ApexCharts(document.querySelector("#chart2"), options2);

chart2.render().then(() => {
	getData2();
});
