
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

function setCart(item, op) {
    let cart = getCart();
    if (cart[item]) {
        cart[item] += op;
    } else {
        cart[item] = 1
    }
    const cartJSON = JSON.stringify(cart);
    document.cookie = `cart=${cartJSON}; expires=${getDateString(7)}; path=/`;
}

function increment(input) {
    input.value += 1;
    setCart(input.name, +1);
    window.location.reload();
}

function decrement(input) {
    if (input.value > 1) {
        input.value -= 1;
        setCart(input.name, -1);
        window.location.reload();
    } else {
        alert("value can't be less than 1");
    }
}
