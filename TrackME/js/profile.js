 
// Pie / Doughnut Chart
var ctx = document.getElementById('pie-chart').getContext('2d');
var monthlyData = [
    //{{ categories.Food }},
    //{{ categories.Transportation }},
    //{{ categories.Clothing }},
    //{{ categories.Utilities }},
    //{{ categories.Groceries }},
    //{{ categories.Others }}
];

var config = {
    type: 'doughnut',
    data: {
        datasets: [{
            data: monthlyData,
            backgroundColor: [
                '#C40C0C', '#40A578', '#4B70F5', '#9BCF53', '#F2AFEF', '#F99417'
            ],
            label: 'Expenses'
        }],
        labels: ['Food', 'Transportation', 'Clothing', 'Utilities', 'Groceries', 'Others']
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Spending Disparity: //{{this_month}}'
            },
            legend: {
            }
        }
    }
};

var pieChart = new Chart(ctx, config);

// Dropdown menu code to change pie chart into yearly distribution or monthly
const change = document.getElementById('time');
change.addEventListener('change', function() {
    if (change.value === 'year') { // Yearly Dataset
        pieChart.data.datasets[0].data = [
            //{{ percentage_yearly.Food }},
            //{{ percentage_yearly.Transportation }},
            //{{ percentage_yearly.Clothing }},
            //{{ percentage_yearly.Utilities }},
            //{{ percentage_yearly.Groceries }},
            //{{ percentage_yearly.Others }},
        ];
        pieChart.options.plugins.title.text = 'Spending Disparity: //{{this_year}}';
    } 
    
    else { // Monthly Dataset
        pieChart.data.datasets[0].data = [
            //{{ categories.Food }},
            //{{ categories.Transportation }},
            //{{ categories.Clothing }},
            //{{ categories.Utilities }},
            //{{ categories.Groceries }},
            //{{ categories.Others }},
        ];
        pieChart.options.plugins.title.text = 'Spending Disparity: //{{this_month}} //{{ this_year }}';
    }

    pieChart.update();
});



 // Bar Chart
var ctxYearly = document.getElementById('yearly-bar-chart').getContext('2d');

var yearlyData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'],
    datasets: [{
        label: '//{{year}} Spending',
        data: [
            //{{ bar_graph_data.Jan }},
            //{{ bar_graph_data.Feb }},
            //{{ bar_graph_data.Mar }},
            //{{ bar_graph_data.Apr }},
            //{{ bar_graph_data.May }},
            //{{ bar_graph_data.Jun }},
            //{{ bar_graph_data.Jul }},
            //{{ bar_graph_data.Aug }},
            //{{ bar_graph_data.Sept }},
            //{{ bar_graph_data.Oct }},
            //{{ bar_graph_data.Nov }},
            //{{ bar_graph_data.Dec }}
        ],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
    }]
};

var configYearly = {
    type: 'bar',
    data: yearlyData,
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            title: {
                display:true,
                text: "Yearly Spending"
            }
        }
    }
};

new Chart(ctxYearly, configYearly);



// Sidebar toggle and dark mode logic
const body = document.querySelector('body'),
sidebar = body.querySelector('nav'),
toggle = body.querySelector(".toggle"),
modeSwitch = body.querySelector(".toggle-switch"),
modeText = body.querySelector(".mode-text");

toggle.addEventListener("click", () => {
sidebar.classList.toggle("close");
});

searchBtn.addEventListener("click", () => {
sidebar.classList.remove("close");
});

// Check for saved theme preference on page load
document.addEventListener('DOMContentLoaded', (event) => {
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {
    document.body.classList.add(savedTheme);

    if (savedTheme === 'dark') {
        modeText.innerText = "Light mode";
    } 
    else {
        modeText.innerText = "Dark mode";
    }
}
});

modeSwitch.addEventListener("click", () => {
if (document.body.classList.contains("dark")) {
    document.body.classList.remove("dark");
    localStorage.setItem('theme', '');
    modeText.innerText = "Dark mode";
} 
else {
    document.body.classList.add("dark");
    localStorage.setItem('theme', 'dark');
    modeText.innerText = "Light mode";
}
});


// Transaction form toggle
let transaction = document.getElementById('add_transaction');
let elementArray = document.getElementsByClassName('add_transaction');
let cancelbtn = document.getElementById('cancel');

transaction.addEventListener('click', () => {
for (let i = 0; i < elementArray.length; i++) {
    elementArray[i].style.display = 'inline-block';
    transaction.style.display = 'none'
}
});

cancelbtn.addEventListener('click', () => {
for (let i = 0; i <elementArray.length; i++) {
    elementArray[i].style.display = 'none';
    transaction.style.display = 'inline-block'
}
});

let subion = document.getElementById('add_subsion');
let elementArray2 = document.getElementsByClassName('add_subsion');
let cancelbtn2 = document.getElementById('cancel2');

subion.addEventListener('click', () => {
for (let i = 0; i < elementArray2.length; i++) {
    elementArray2[i].style.display = 'inline-block';
    subion.style.display = 'none'
}
});

cancelbtn2.addEventListener('click', () => {
for (let i = 0; i<elementArray2.length; i++) {
    elementArray2[i].style.display = 'none';
    subion.style.display = 'inline-block'

}
});