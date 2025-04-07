window.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('summaryChart');

    if (ctx) {
        const income = parseFloat(ctx.dataset.income) || 0;
        const expense = parseFloat(ctx.dataset.expense) || 0;
        const total = income + expense;
        const chartData = total === 0 ? [1, 0] : [income, expense];

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Income', 'Expense'],
                datasets: [{
                    data: chartData,
                    backgroundColor: ['#28a745', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
});
