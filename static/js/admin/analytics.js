/* global Chart, stats */
// (provided by Chart.js and Django, respectively)

(() => {
  const createDatatypeInterestChart = (data) => {
    new Chart(document.getElementById('queried-datatypes'), {
      type: 'bar',
      data: {
        labels: data.map(([datatype]) => datatype),
        datasets: [
          {
            label: 'Queries',
            data: data.map(([, { queries }]) => queries),
          },
          {
            label: 'Views',
            data: data.map(([, { views }]) => views),
          },
        ],
      },
      options: {
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
        responsive: false,
        plugins: {
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                const tooltip = `${tooltipItem.dataset.label}: ${tooltipItem.formattedValue}`;
                // If one of the datasets is hidden, the percentage value is confusing
                if (
                  tooltipItem.chart.data.datasets.some(({ hidden }) => hidden)
                ) {
                  return tooltip;
                }
                const total = tooltipItem.chart.data.datasets.reduce(
                  (sum, dataset) => dataset.data[tooltipItem.dataIndex] + sum,
                  0
                );
                const percentage = tooltipItem.raw / total;
                const formattedPercentage = Math.round(percentage * 100);
                return `${tooltip} (${formattedPercentage} %)`;
              },
            },
          },
          legend: {
            onClick: (event, legendItem) => {
              event.chart.data.datasets[legendItem.datasetIndex].hidden =
                !event.chart.data.datasets[legendItem.datasetIndex].hidden;
              // Resort the data based on the *visible* datasets
              const scoringFns = event.chart.data.datasets.map((dataset, i) => {
                if (dataset.hidden) {
                  return () => 0;
                }
                if (i === 0) {
                  return ({ queries }) => queries;
                }
                // i === 1
                return ({ views }) => views;
              });
              const scoreItem = (item) =>
                scoringFns
                  .map((scoringFn) => scoringFn(item)) // map each fn to a score
                  .reduce((total, value) => total + value); // calculate the total score
              const sortedData = data
                .slice()
                .sort(([, a], [, b]) => scoreItem(b) - scoreItem(a));
              event.chart.data.labels = sortedData.map(([label]) => label);
              event.chart.data.datasets[0].data = sortedData.map(
                ([, { queries }]) => queries
              );
              event.chart.data.datasets[1].data = sortedData.map(
                ([, { views }]) => views
              );
              event.chart.update();
            },
          },
        },
      },
    });
  };

  const createDatatypeDetailCharts = (datatype, data) => {
    ['sources', 'destinations', 'transitions'].forEach((queryCountName) => {
      const previousChart = Chart.getChart(`datatype-${queryCountName}`);
      if (previousChart) {
        previousChart.destroy();
      }

      const sortedData =
        data && data[queryCountName]
          ? Object.entries(data[queryCountName])
              .slice()
              .sort(([, a], [, b]) => b - a)
          : [];

      new Chart(document.getElementById(`datatype-${queryCountName}`), {
        type: 'bar',
        data: {
          labels: sortedData.map(([datatype]) => datatype),
          datasets: [
            {
              label: 'Queries',
              data: sortedData.map(([, queryCount]) => queryCount),
            },
          ],
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: `Queried ${datatype} ${queryCountName}`,
            },
          },
          responsive: false,
        },
      });
    });
  };

  document.addEventListener('DOMContentLoaded', () => {
    const data = Object.entries(stats.datatypeInterest)
      .slice()
      // Sort them by descending interest (queries + views)
      .sort(
        ([, aCounts], [, bCounts]) =>
          bCounts.views + bCounts.queries - aCounts.views - aCounts.queries
      );

    createDatatypeInterestChart(data);

    const tabList = document.getElementById('src-dest-tab-list');
    data.forEach(([datatype], i) => {
      const buttonEl = document.createElement('button');
      buttonEl.innerText = datatype;
      buttonEl.addEventListener('click', () => {
        createDatatypeDetailCharts(
          datatype,
          stats.providerQueriesByDatatype[datatype]
        );
      });
      const liEl = document.createElement('li');
      liEl.append(buttonEl);
      tabList.append(liEl);
      if (i === 0) {
        buttonEl.click();
      }
    });
  });
})();
