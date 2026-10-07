/**
 * ==============================================================================
 * IPL Statistical Analysis - Reusable Chart.js Factory
 * ==============================================================================
 * Standardizes styling, dark mode grids, responsive scaling, and safe chart updates.
 * ==============================================================================
 */

// Store active chart instances by canvas ID so we can safely destroy and update them
const chartInstances = {};

// Default dark theme options for Chart.js
Chart.defaults.color = '#94a3b8';
Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";

function getCommonChartOptions(titleText = '') {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#cbd5e1',
          font: { size: 12, weight: 500 }
        }
      },
      tooltip: {
        backgroundColor: '#0f172a',
        titleColor: '#00e5ff',
        bodyColor: '#ffffff',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8
      },
      title: {
        display: !!titleText,
        text: titleText,
        color: '#f8fafc',
        font: { size: 14, weight: 600 }
      }
    },
    scales: {
      x: {
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
        ticks: { color: '#94a3b8' }
      },
      y: {
        grid: { color: 'rgba(255, 255, 255, 0.05)' },
        ticks: { color: '#94a3b8' }
      }
    }
  };
}

/**
 * Creates or updates a Bar Chart
 */
function renderBarChart(canvasId, labels, data, datasetLabel = 'Value', bgColors = '#00e5ff') {
  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  chartInstances[canvasId] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: datasetLabel,
        data: data,
        backgroundColor: bgColors,
        borderRadius: 6,
        borderSkipped: false
      }]
    },
    options: getCommonChartOptions()
  });

  return chartInstances[canvasId];
}

/**
 * Creates or updates a Line Chart
 */
function renderLineChart(canvasId, labels, data, datasetLabel = 'Trend', borderColor = '#00e5ff') {
  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  chartInstances[canvasId] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: datasetLabel,
        data: data,
        borderColor: borderColor,
        backgroundColor: 'rgba(0, 229, 255, 0.1)',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: borderColor,
        pointRadius: 4
      }]
    },
    options: getCommonChartOptions()
  });

  return chartInstances[canvasId];
}

/**
 * Creates or updates a Doughnut / Pie Chart
 */
function renderDoughnutChart(canvasId, labels, data, colors = ['#00e5ff', '#3b82f6', '#10b981', '#f59e0b', '#ec4899']) {
  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  const options = getCommonChartOptions();
  // Doughnuts don't have x/y scales
  delete options.scales;

  chartInstances[canvasId] = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: colors,
        borderWidth: 2,
        borderColor: '#111827'
      }]
    },
    options: options
  });

  return chartInstances[canvasId];
}

/**
 * Creates a Grouped Bar Chart (for comparison)
 */
function renderGroupedBarChart(canvasId, labels, datasets) {
  if (chartInstances[canvasId]) {
    chartInstances[canvasId].destroy();
  }

  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;

  chartInstances[canvasId] = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: getCommonChartOptions()
  });

  return chartInstances[canvasId];
}
