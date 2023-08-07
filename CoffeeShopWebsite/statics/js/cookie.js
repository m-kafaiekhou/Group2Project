
function getDateString(daysForward=0) {
    const date = new Date();
    date.setDate(date.getDate() + daysForward);
    return date.toUTCString();
}

function getCart() {
    let cartCookie = document.cookie.replace(
        /(?:(?:^|.*;\s*)cart\s*=\s*([^;]*).*$)|^.*$/, "$1"
    );
    if (cartCookie == "") {
        cartCookie = JSON.stringify({});
    }
    const cart = JSON.parse(cartCookie);
    return cart;
}

function setCart(item, quantity) {
    let cart = getCart();
    cart[item] = +quantity;
    const cartJSON = JSON.stringify(cart);
    document.cookie = `cart=${cartJSON}; expires=${getDateString(7)}; path=/`;
}

function increment(input) {
    const item = input.name;
    const value = parseInt(input.value);
    input.value = value + 1;
    setCart(item, input.value);
}

function decrement(input) {
    const item = input.name;
    const value = parseInt(input.value);
    if (value > 1) {
        input.value = value - 1;
        setCart(item, input.value);
    } else {
        alert("value can't be less than 1");
    }
}
