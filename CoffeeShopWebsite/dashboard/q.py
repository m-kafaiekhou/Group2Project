from coffeeshop.models import *
from menus.models import *
from orders.models import *
from staff.models import *
from datetime import datetime, timedelta
from django.db.models import Sum,Avg

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
    # return CafeItem.objects.raw(sql, [start_date, end_date, num])
    queryset = CafeItem.objects.filter(
        orderitem__order__order_date__gt=start_date,
        orderitem__order__order_date__lt=end_date
    ).values('orderitem__cafeitem__name').annotate(
        total_quantity=Sum('orderitem__quantity')
    ).order_by('-total_quantity')[:num]
    return queryset

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
    #return CafeItem.objects.raw(sql, [start_date, end_date, num])

    queryset = CafeItem.objects.filter(
        orderitem__order__order_date__gt=start_date,
        orderitem__order__order_date__lt=end_date
    ).values('orderitem__cafeitem__name').annotate(
        avg_rating=Avg('coffeeshop_review__rating')
    ).order_by('-avg_rating')[:num]
    return queryset

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
    #return Category.objects.raw(sql, [start_date, end_date, num])
    queryset = Order.objects.filter(order_date__gt=start_date, order_date__lt=end_date) \
                   .select_related('orderitem__cafeitem__review', 'orderitem__cafeitem__category') \
                   .values('orderitem__cafeitem__category__name') \
                   .annotate(avg_rating=Avg('orderitem__cafeitem__review__rating')) \
                   .order_by('-avg_rating')[:num]
    return queryset

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
    #return Category.objects.raw(sql, [start_date, end_date, num])
    queryset = Category.objects.filter(
        cafeitem__orderitem__order__order_date__gt=start_date,
        cafeitem__orderitem__order__order_date__lt=end_date
    ).annotate(
        total_quantity=Sum('cafeitem__orderitem__quantity')
    ).values(
        'name', 'total_quantity'
    ).order_by(
        '-total_quantity'
    )[:num]
    return queryset

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
    #return Order.objects.raw(sql, [start_date, end_date, num])
    queryset = Order.objects.filter(
        order_date__gt=start_date,
        order_date__lt=end_date
    ).annotate(
        total_price=Sum('orderitem__price')
    ).order_by('-total_price')[:num]

    return [(order.phone_number, order.total_price) for order in queryset]


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
    #return CafeItem.objects.raw(sql, [start_date, end_date, cafe_item])
    queryset = CafeItem.objects.filter(
        orderitem__order__order_date__gt=start_date,
        orderitem__order__order_date__lt=end_date,
        name=cafe_item
    ).annotate(total_quantity=Sum('orderitem__quantity')).order_by('-total_quantity')

    return [(item.name, item.total_quantity) for item in queryset]


def amount_of_sold_coffeshop_items_total_price_in_a_period_of_time(start_date, end_date):
    sql = '''
        select sum(orders_orderitem.price)
        from orders_order inner join orders_orderitem
        on orders_order.id = orders_orderitem.order_id 
        where orders_order.order_date > %s and orders_order.order_date < %s
        '''
    #return OrderItem.objects.raw(sql, [start_date, end_date])
    total_price = Order.objects.filter(order_date__gt=start_date, order_date__lt=end_date) \
        .annotate(total_price=Sum('orderitem__price')).values('total_price')
    return total_price


def amount_of_sold_coffeshop_items_total_price_in_a_period_of_time_by_a_customer(start_date, end_date, phone_number):
    sql = '''
        select sum(orders_orderitem.price)
        from orders_order inner join orders_orderitem
        on orders_order.id = orders_orderitem.order_id 
        where orders_order.order_date > %s and orders_order.order_date < %s and orders_order.phone_number = %s
        '''
    #return OrderItem.objects.raw(sql, [start_date, end_date, phone_number])
    total_price = OrderItem.objects.filter(order__order_date__gt=start_date,
                                           order__order_date__lt=end_date,
                                           order__phone_number=phone_number).aggregate(Sum('price'))
    return total_price

def soled_cafe_items_to_a_customer_in_a_period_of_time(start_date, end_date, phone_number):
    sql = '''
        select menus_cafeitem.name
        from menus_cafeitem inner join orders_orderitem
        on menus_cafeitem.id = orders_orderitem.cafeitem_id
        inner join orders_order
        on orders_order.id = orders_orderitem.order_id
        where orders_order.order_date > %s and orders_order.order_date < %s and orders_order.phone_number = %s;
        '''
    return CafeItem.objects.raw(sql, [start_date, end_date, phone_number])


print(most_selled_cafe_items_in_a_peroid_of_time('2023-01-23 00:00:00','2023-08-12',2))

