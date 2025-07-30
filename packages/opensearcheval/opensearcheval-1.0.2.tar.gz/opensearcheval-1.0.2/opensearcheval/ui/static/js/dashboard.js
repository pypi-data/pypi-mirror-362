// Dashboard functionality

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  initDashboard();
});

async function initDashboard() {
  // Load dashboard data
  try {
    const data = await API.get('v1/dashboard');
    updateDashboard(data);
    
    // Set up refresh button
    const refreshButton = document.getElementById('refresh-data');
    if (refreshButton) {
      refreshButton.addEventListener('click', async () => {
        refreshButton.disabled = true;
        try {
          const newData = await API.get('v1/dashboard');
          updateDashboard(newData);
          showNotification('Dashboard refreshed successfully');
        } catch (error) {
          // Error handling is done in the API helper
        } finally {
          refreshButton.disabled = false;
          document.getElementById('last-updated').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        }
      });
    }
  } catch (error) {
    console.error('Error initializing dashboard:', error);
  }
}

function updateDashboard(data) {
  // Update summary metrics
  updateSummaryMetrics(data.summary);
  
  // Update performance chart
  updatePerformanceChart(data.performance);
  
  // Update latest experiments table
  updateExperimentsTable(data.experiments);
  
  // Update recent evaluations table
  updateEvaluationsTable(data.evaluations);
}

function updateSummaryMetrics(summary) {
  if (!summary) return;
  
  // Update total experiments
  const totalExperimentsEl = document.getElementById('total-experiments');
  if (totalExperimentsEl) {
    totalExperimentsEl.textContent = summary.totalExperiments || 0;
  }
  
  // Update running experiments
  const runningExperimentsEl = document.getElementById('running-experiments');
  if (runningExperimentsEl) {
    runningExperimentsEl.textContent = summary.runningExperiments || 0;
  }
  
  // Update completed experiments
  const completedExperimentsEl = document.getElementById('completed-experiments');
  if (completedExperimentsEl) {
    completedExperimentsEl.textContent = summary.completedExperiments || 0;
  }
  
  // Update API status
  const apiStatusEl = document.getElementById('api-status');
  if (apiStatusEl) {
    apiStatusEl.textContent = summary.apiStatus || 'Unknown';
    
    // Set color based on status
    if (summary.apiStatus === 'Healthy') {
      apiStatusEl.style.color = 'var(--success-color)';
    } else {
      apiStatusEl.style.color = 'var(--danger-color)';
    }
  }
}

function updatePerformanceChart(performance) {
  if (!performance || !performance.dates || !performance.metrics) return;
  
  const chartContainer = document.getElementById('performance-chart');
  if (!chartContainer) return;
  
  // Create traces for each metric
  const traces = [];
  
  for (const metricName in performance.metrics) {
    traces.push({
      x: performance.dates,
      y: performance.metrics[metricName],
      type: 'scatter',
      mode: 'lines+markers',
      name: metricName,
      line: {
        width: 3
      }
    });
  }
  
  const layout = {
    margin: { t: 10, r: 10, b: 40, l: 50 },
    xaxis: {
      title: 'Date',
      tickformat: '%Y-%m-%d'
    },
    yaxis: {
      title: 'Value'
    },
    legend: {
      orientation: 'h',
      y: -0.2
    },
    autosize: true,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      family: 'Inter, sans-serif'
    }
  };
  
  Plotly.newPlot(chartContainer, traces, layout, {
    responsive: true,
    displayModeBar: false
  });
}

function updateExperimentsTable(experiments) {
  const tableBody = document.querySelector('#latest-experiments-table tbody');
  if (!tableBody || !experiments || !experiments.length) {
    if (tableBody) {
      tableBody.innerHTML = '<tr><td colspan="4" class="loading-message">No experiments found</td></tr>';
    }
    return;
  }
  
  // Clear table
  tableBody.innerHTML = '';
  
  // Add rows for each experiment
  experiments.forEach(experiment => {
    const row = document.createElement('tr');
    
    // Create table cells
    const nameCell = document.createElement('td');
    const nameLink = document.createElement('a');
    nameLink.href = `/experiments/${experiment.id}`;
    nameLink.textContent = experiment.name;
    nameCell.appendChild(nameLink);
    
    const statusCell = document.createElement('td');
    const statusBadge = document.createElement('span');
    statusBadge.className = `badge badge-${getStatusClass(experiment.status)}`;
    statusBadge.textContent = experiment.status;
    statusCell.appendChild(statusBadge);
    
    const createdCell = document.createElement('td');
    createdCell.textContent = formatDate(experiment.created_at);
    
    const actionsCell = document.createElement('td');
    const viewButton = document.createElement('a');
    viewButton.href = `/experiments/${experiment.id}`;
    viewButton.className = 'btn btn-small btn-primary';
    viewButton.textContent = 'View';
    actionsCell.appendChild(viewButton);
    
    // Add cells to row
    row.appendChild(nameCell);
    row.appendChild(statusCell);
    row.appendChild(createdCell);
    row.appendChild(actionsCell);
    
    // Add row to table
    tableBody.appendChild(row);
  });
}

function updateEvaluationsTable(evaluations) {
  const tableBody = document.querySelector('#recent-evaluations-table tbody');
  if (!tableBody || !evaluations || !evaluations.length) {
    if (tableBody) {
      tableBody.innerHTML = '<tr><td colspan="4" class="loading-message">No evaluations found</td></tr>';
    }
    return;
  }
  
  // Clear table
  tableBody.innerHTML = '';
  
  // Add rows for each evaluation
  evaluations.forEach(evaluation => {
    const row = document.createElement('tr');
    
    // Create table cells
    const queryCell = document.createElement('td');
    queryCell.textContent = truncateText(evaluation.query, 30);
    
    const mrrCell = document.createElement('td');
    mrrCell.textContent = evaluation.metrics.mrr?.toFixed(3) || 'N/A';
    
    const ctrCell = document.createElement('td');
    ctrCell.textContent = evaluation.metrics.ctr?.toFixed(3) || 'N/A';
    
    const timeCell = document.createElement('td');
    timeCell.textContent = formatDate(evaluation.timestamp);
    
    // Add cells to row
    row.appendChild(queryCell);
    row.appendChild(mrrCell);
    row.appendChild(ctrCell);
    row.appendChild(timeCell);
    
    // Add row to table
    tableBody.appendChild(row);
  });
}

function getStatusClass(status) {
  switch (status.toLowerCase()) {
    case 'running':
      return 'success';
    case 'completed':
      return 'primary';
    case 'paused':
      return 'warning';
    case 'failed':
      return 'danger';
    default:
      return 'secondary';
  }
}