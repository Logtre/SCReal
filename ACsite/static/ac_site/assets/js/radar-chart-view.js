console.log('***DEBUG***');
console.log(document);

var ctx = document.getElementById('radar-chart-content').getContext('2d');
var mychart =  new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ['訪問客数', '売上予想', '年間の売上変動', '競合数', '物件購入費', '利益予想'],
        datasets: [{
            label: 'レーティング',
            data: [{{marketsize}}, {{potential}}, {{stability}}, {{conpetition}}, {{price}}, {{ex_return}}],
            backgroundColor: "rgba(52,199,23,0.6)"
        }]
    },
    options: {
        legend: {
            display: false
        },
        scale: {
            ticks: {
                beginAtZero: true,
                max: 5,
            }
        }
        //scaleShowLine: true,
        //scaleOverride: true,
        //scaleSteps: 10,
        //scaleStepWidth: 1,
        //scaleStartValue: 0
    }
});
//new Chart(ctx).Radar(myChart);
