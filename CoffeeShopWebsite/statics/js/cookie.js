
function getDateString(daysForward=0) {
    const date = new Date();
    date.setDate(date.getDate() + daysForward);
    return date.toUTCString();
}

function getCart() {
    const cartCookie = document.cookie.replace(/((?:^|.*;\s*)cart\s*=\s*([^;]*).*$)|^.*$/, "$1");
    const cart = JSON.parse(cartCookie);
    return cart;
}

function setCart() {

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


