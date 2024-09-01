function initializeCharts() {
    if (document.querySelector('#occupancyChart')) {
        const ctx = document.getElementById('occupancyChart').getContext('2d');

        const maxValues = [102, 114, 84];
        const usedValues = [{{ occupancy.0 }}, {{ occupancy.1 }}, {{ occupancy.2 }}];
        const labels = ['Cluster 1', 'Cluster 2', 'Cluster 3'];

        const percentages = usedValues.map((value, index) => (value / maxValues[index]) * 100);

        function interpolateColor(percent) {
            const startColor = [54, 162, 235];
            const endColor = [255, 0, 0];

            const r = Math.round(startColor[0] + percent * (endColor[0] - startColor[0]) / 100);
            const g = Math.round(startColor[1] + percent * (endColor[1] - startColor[1]) / 100);
            const b = Math.round(startColor[2] + percent * (endColor[2] - startColor[2]) / 100);

            return `rgba(${r}, ${g}, ${b}, 0.2)`;
        }

        const colors = percentages.map(percent => interpolateColor(percent));

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Occupancy (%)',
                    data: percentages,
                    backgroundColor: colors,
                    borderColor: colors.map(color => color.replace('0.2', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        },
                        title: {
                            display: true,
                            text: 'Percentage'
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const index = context.dataIndex;
                                return `Used: ${usedValues[index]} / ${maxValues[index]} (${context.raw.toFixed(2)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
}

// Initialize charts on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

// Reinitialize charts after HTMX content swap
document.addEventListener('htmx:afterSwap', function() {
    initializeCharts();
});
