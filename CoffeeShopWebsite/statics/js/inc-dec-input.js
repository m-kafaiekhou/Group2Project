function increment() {
    var input = document.getElementById('quantity');
    var value = parseInt(input.value);
    input.value = value + 1;
}

function decrement() {
    var input = document.getElementById('quantity');
    var value = parseInt(input.value);
    if (value > 0) {
        input.value = value - 1;
    }
}
