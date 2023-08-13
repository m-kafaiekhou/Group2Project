from django.shortcuts import render, redirect
from django.contrib import messages
from orders.models import Order
from melipayamak import Api
import random
import environ
import datetime

env = environ.Env()
environ.Env.read_env()


def delete_cart(request, response) -> None:
    if request.COOKIES.get("cart"):
        response.delete_cookie("cart")


def create_session(request, order_id: int, phone_number: int) -> None:
    request.session["last_order_id"] = order_id
    request.session["phone_number"] = phone_number


def access_session(request):
    """
    checks if the session exists and then returnes a context containing
    order_history and last_order.

    if it does not exist an empty context will be returned.
    """
    if "last_order_id" and "phone_number" in request.session:
        order_id = request.session.get("last_order_id")
        last_order = Order.objects.get(pk=order_id)

        phone_number = request.session.get("phone_number")
        orders = Order.objects.filter(phone_number=phone_number)

        context = {"order_history": orders, "last_order": last_order}
        return render(request, "", context)
    else:
        context = {}
        return render(request, "", context)


def send_otp_code(phone_number, code):
    print("*" * 120)
    print("Verification Code:")
    print(f"{phone_number}: {code}")
    print("*" * 120)

    username = env("OTP_USERNAME")
    password = env("OTP_PASSWORD")
    api = Api(username, password)
    sms = api.sms()
    to = phone_number
    _from = "50004001018172"
    text = f"کد تایید شما: {code}"
    response = sms.send(to, _from, text)
    print(response)


def set_otp(request, phone_number):
    random_code = random.randint(1000, 9999)
    send_otp_code(phone_number=phone_number, code=random_code)
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
    request.session["phone_number"] = phone_number
    request.session["otp_code"] = random_code
    messages.success(request, "کد تایید به شماره موبایل شما ارسال شد", "success")
    return redirect("code_entry")


# def add_to_cart(request, response, item_pk: int) -> None:
#     """
#     sets a cookie to add items to shopping cart.
#
#     item_pk and quantity turn into a list of dictionaries which is the
#     value of the cart cookie.
#     value = [{menu_item:quantity}, ...]
#     """
#     cart = request.COOKIES.get("cart", None)
#     if not cart:
#         value = list()
#         value.append({f"{item_pk}": 1})
#         str_value = f"{value}"
#         max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
#         response.set_cookie("cart", str_value, max_age=max_age)
#     else:
#         cart = eval(cart)
#         old_val = 0
#         # print(cart, "_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
#         for i in range(len(cart)):
#             print(i, "_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
#             for key, val in cart[i].items():
#                 # print(key, val, cart[i], "_*_*_*_*_*_*_*_*_*_*_*_*_*_*_*_")
#                 if key == item_pk:
#                     old_val = val
#                     cart.pop(i)
#             if old_val == val:
#                 break
#         item_dict = {item_pk: old_val + 1}
#         cart.append(item_dict)
#         str_value = f"{cart}"
#         max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
#         response.set_cookie("cart", str_value, max_age=max_age)
#     return response


# def remove_from_cart(request, response, item_pk: int):
#     """
#     remove an item from the shopping cart, completely.
#     """
#     if request.COOKIES.get("cart"):
#         v = request.COOKIES.get("cart")
#         value = eval(v)
#         for i in range(value):
#             if value[i].key == item_pk:
#                 value.pop(i)
#         delete_cart(request, response)
#
#         str_value = f"{value}"
#         max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
#         response.set_cookie("cart", str_value, max_age=max_age)


# def update_cart(request, response, item_pk: int, quantity: int):
#     """
#     updates the quantity of each item in the shopping cart.
#     """
#
#     if request.COOKIES.get("cart"):
#         v = request.COOKIES.get("cart")
#         cart = eval(v)
#         for i in range(len(cart)):
#             for key, val in cart[i].items():
#                 if int(key) == item_pk:
#                     cart.append({f"{item_pk}": quantity})
#                     cart.pop(i)
#         delete_cart(request, response)
#
#         str_value = f"{cart}"
#         max_age = 604800  # 7 * 24 * 60 * 60 (7 days)
#         response.set_cookie("cart", str_value, max_age=max_age)
#         return response
