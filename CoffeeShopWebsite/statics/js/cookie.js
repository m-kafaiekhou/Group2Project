
function getCookie() {

}



function increment(input) {
    var name = input.name;
    var value = parseInt(input.value);
    input.value = value + 1;
}

function decrement(input) {
    var name = input.name;
    var value = parseInt(input.value);
    if (value > 1) {
        input.value = value - 1;
    }
}


