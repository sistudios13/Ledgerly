let rawData = [];

async function getData() {
	const accountId = Alpine.store("ledgerly").balance_chart_account;
	rawData = await window.pywebview.api.get_balance_over_time(accountId);

	rawData = rawData.map((item) => ({
		x: item.date,
		y: Number(item.value),
	}));

	if (typeof chart !== "undefined") {
		chart.updateSeries([
			{
				name: "Account Balance",
				data: rawData,
			},
		]);
	}
}

window.getData = getData;

async function getData2() {
	const accountId2 = Alpine.store("ledgerly").category_chart_account;
	rawData2 = await window.pywebview.api.get_total_by_category(accountId2, "expense");

	if (rawData2 && rawData2.length >= 2) {
		let values = rawData2[0];
		let labels = rawData2[1];

		if (chart2) {
            if (values.every(v => v == 0)) {
                values = [1];
                labels = ["No Data"];
            }
			chart2.updateOptions({
				series: values,
				labels: labels,
			});
		}
	}
}

window.getData2 = getData2;
