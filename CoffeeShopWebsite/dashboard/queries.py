from coffeeshop.models import *
from menus.models import *
from orders.models import *
from staff.models import *
from datetime import datetime, timedelta

def most_selled_cafe_items_in_a_peroid_of_time(start_date, end_date, num):
    sql = '''
    select menus_cafeitem.name, sum(orders_orderitem.quantity)
    from menus_cafeitem inner join orders_orderitem
    on menus_cafeitem.id = orders_orderitem.cafeitem_id
    inner join orders_order
    on orders_order.id = orders_orderitem.order_id
    where orders_order.order_date > %s and orders_order.order_date < %s
    group by menus_cafeitem.name
    order by sum(orders_orderitem.quantity) desc
    limit %s;
    '''
    return CafeItem.objects.raw(sql, [start_date, end_date, num])

def most_popular_cafe_items_in_a_peroid_of_time(start_date, end_date, num):
    sql = '''
    select menus_cafeitem.name, avg(coffeeshop_review.rating)
    from orders_order inner join orders_orderitem
    on orders_order.id = orders_orderitem.order_id 
    inner join menus_cafeitem
    on menus_cafeitem.id = orders_orderitem.cafeitem_id
    inner join coffeeshop_review 
    on coffeeshop_review.cafeitem_id = menus_cafeitem.id
    where orders_order.order_date > %s and orders_order.order_date < %s
    group by menus_cafeitem.name
    order by avg(coffeeshop_review.rating) desc
    limit %s;
    '''
    return CafeItem.objects.raw(sql, [start_date, end_date, num])

def most_popular_categories_in_a_peroid_of_time(start_date, end_date, num):
    sql = '''
    select menus_category.name, avg(coffeeshop_review.rating)
    from orders_order inner join orders_orderitem
    on orders_order.id = orders_orderitem.order_id 
    inner join menus_cafeitem
    on menus_cafeitem.id = orders_orderitem.cafeitem_id
    inner join coffeeshop_review 
    on coffeeshop_review.cafeitem_id = menus_cafeitem.id
    inner join menus_category
    on menus_category.cafeitem_id = menus_cafeitem.id
    where orders_order.order_date > %s and orders_order.order_date < %s
    group by menus_category.name
    order by avg(coffeeshop_review.rating) desc
    limit %s;
    '''
    return Category.objects.raw(sql, [start_date, end_date, num])

def most_selled_categories_in_a_peroid_of_time(start_date, end_date, num):
    sql = '''
    select menus_category.name, sum(orders_orderitem.quantity)
    from menus_cafeitem inner join orders_orderitem
    on menus_cafeitem.id = orders_orderitem.cafeitem_id
    inner join orders_order
    on orders_order.id = orders_orderitem.order_id
    inner join menus_category
    on menus_category.cafeitem_id = menus_cafeitem.id
    where orders_order.order_date > %s and orders_order.order_date < %s
    group by menus_category.name
    order by sum(orders_orderitem.quantity) desc
    limit %s;
    '''
    return Category.objects.raw(sql, [start_date, end_date, num])

def best_customers_in_a_peroid_of_time(start_date, end_date, num):
    sql = '''
    select orders_order.phone_number, sum(orders_orderitem.price)
    from orders_order inner join orders_orderitem
    on orders_order.id = orders_orderitem.order_id 
    where orders_order.order_date > %s and orders_order.order_date < %s
    group by orders_order.phone_number
    order by sum(orders_orderitem.price) desc
    limit %s;
    '''
    return Order.objects.raw(sql, [start_date, end_date, num])

def number_of_a_selled_cafe_item_in_a_peroid_of_time(start_date, end_date, cafe_item):
    sql = '''
    select menus_cafeitem.name, sum(orders_orderitem.quantity)
    from orders_order inner join orders_orderitem
    on orders_order.id = orders_orderitem.order_id 
    inner join menus_cafeitem
    on menus_cafeitem.id = orders_orderitem.cafeitem_id
    where orders_order.order_date > %s and orders_order.order_date < %s
    group by menus_cafeitem.name
    having menus_cafeitem.name = %s
    order by sum(orders_orderitem.quantity) desc ;
    '''
    return CafeItem.objects.raw(sql, [start_date, end_date, cafe_item])