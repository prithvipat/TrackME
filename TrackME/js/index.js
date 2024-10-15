        var ctx = document.getElementById('pie-chart').getContext('2d');
        
        // Assuming the 'categories' is a dictionary, we need to pass the values as an array
        var dataValues = [
            //{{categories.Food}},
            //{{categories.Transportation}},
            //{{categories.Clothing}},
            //{{categories.Utilities}},
            //{{categories.Groceries}},
            //{{categories.Others}}
        ];
        
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: dataValues,
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
                    legend: {
                        display: false
                    }
                }
            }

        };
        new Chart(ctx, config);

        
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
                } else {
                    modeText.innerText = "Dark mode";
                }
            }
        });
        

        modeSwitch.addEventListener("click", () => {
            if (document.body.classList.contains("dark")) {
                document.body.classList.remove("dark");
                localStorage.setItem('theme', '');
                modeText.innerText = "Dark mode";
            } else {
                document.body.classList.add("dark");
                localStorage.setItem('theme', 'dark');
                modeText.innerText = "Light mode";
            }
        });
    