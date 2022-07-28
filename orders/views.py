from django.http import JsonResponse
from django.shortcuts import redirect, render
from cart.models import Cart, CartItem
from orders.forms import OrderForm
from .models import Order, OrderProduct, Payment
import datetime
from store.models import Product
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from category.models import MainCategory

# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False,order_number=body['orderID'])

    # store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    # move the cart items to Order product table
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variations = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variations)
        orderproduct.save()

        # reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity

        product.main_category.count_sold += item.quantity
        cat = MainCategory.objects.get(id = product.main_category.id)
        cat.count_sold += item.quantity
        cat.save()
        product.save()


    # clear cart
    CartItem.objects.filter(user=request.user).delete()
 
    # send order recieved email to customer 
    mail_subject = 'Thank You for your order..'
    message = render_to_string('orders/order_recieved_email.html',{
        'user':request.user,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject,message, to=[to_email])
    send_email.send()

    # send order number and transaction id back to sendData method by JsonResponse
    data = {
        'order_number' : order.order_number,
        'transID' : payment.payment_id,

    }
    return JsonResponse(data)


def place_order(request ,total=0,quantity=0):
    current_user = request.user
    # if the cart count is less than  or equal to 0 , then redirect back to shop
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (3 * total )/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid(): 

            # store all the billing information inside order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR') # this will give the user ip
            data.save()

            # generate the order id
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total,

            }
            return render(request, 'orders/payments.html',context)
    else:
        return redirect ('checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)

        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id = transID)
        order_sub_total = order.order_total - order.tax
        context = {
            'order' : order,
            'order_number' : order.order_number,
            'transID' : payment.payment_id,
            'payment' : payment,
            'ordered_products': ordered_products,
            'order_sub_total':order_sub_total,
        }

        return render(request,'orders/order_complete.html',context)   
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect ('home')



             