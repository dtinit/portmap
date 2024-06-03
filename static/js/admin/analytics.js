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
