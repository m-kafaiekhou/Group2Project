
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

function setCart(item) {
    let cart = getCart();
    if (cart[item]) {
        cart[item] += 1;
    } else {
        cart[item] = 1
    }
    const cartJSON = JSON.stringify(cart);
    document.cookie = `cart=${cartJSON}; expires=${getDateString(7)}; path=/`;
}

function increment(input) {
    const item = input.name;
    input.value += 1;
    setCart(item);
    window.location.reload();
}

function decrement(input) {
    const item = input.name;
    if (value > 1) {
        input.value -= 1;
        setCart(item);
        window.location.reload();
    } else {
        alert("value can't be less than 1");
    }
}
