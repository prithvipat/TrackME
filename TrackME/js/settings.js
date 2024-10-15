
let elementArray = document.querySelectorAll("input");
let btn = document.getElementById('budgets-btn')
elementArray.forEach(function(elem) {
    elem.addEventListener('input', function() {
        btn.style.display = 'inline-block';
    });
});