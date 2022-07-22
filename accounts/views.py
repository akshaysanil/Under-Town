
from multiprocessing import context
from django.shortcuts import get_list_or_404, get_object_or_404, render,redirect
from accounts.models import Account
from cart.models import Cart,CartItem
from store.models import Product
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required 

# varification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from orders.models import Order, OrderProduct

from cart.views import _cart_id
# import requests


 
# Create your views here.
def user_register(request):
    if request.method == 'POST':                            
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_no = form.cleaned_data['phone_no']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_no = phone_no
            user.save()


            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate account'
            message = render_to_string('accounts/account_email_verification.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()

            return redirect('/accounts/login/?command=verification&email='+email)
        
    else:

        form=RegistrationForm()
    context={
        'form':form,
    }

    return render(request,'accounts/register2.html',context)

def user_login(request):
    if request.method == 'POST': 
        email=request.POST['email']
        password=request.POST['password']

        user = auth.authenticate(email=email,password=password) 
        
        if user is not None:
                     # for user to use the cart after login 
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter( cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get the cart item from the user to access product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []                     
                    id = []                              
                                                
                    for item in cart_item:               
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request,user)
            messages.success(request,'you are now logged in')
           
            return redirect('home')
        else:
            messages.error(request,'Invalid email or password')
            return redirect('login')

    return render(request,'accounts/login2.html')
login_required(login_url = 'login')



@login_required(login_url="login")
def user_logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out...")
    return redirect ('login')

    

def activate(request,uidb64,token):
    try:
        uid =  urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Your account has been successfully activated.')
        return redirect('login')
    else:
        messages.error(request,'Activation failed try again..!')
        return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id = request.user.id,is_ordered=True)
    orders_count = orders.count()
    UserProfile.objects.get_or_create(user=request.user)
    userprofile = UserProfile.objects.get(user=request.user)
    
    context = {
        'orders_count': orders_count,
        'userprofile' : userprofile,
    }

    return render(request,'accounts/dashboard.html' ,context)



@login_required(login_url='login')
def my_orders(request):
   
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders

    }
    return render(request,'accounts/my_orders.html',context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST ,request.FILES ,instance=userprofile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request,'Your Profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form' :user_form,
        'user_profile_form' : user_profile_form,
        'userprofile' : userprofile,

    }
    return render (request,'accounts/edit_profile.html',context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact = request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Your password has been updated')
                return redirect('change_password')
            else:
                messages.error(request,'Please Enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request,'Password does not match')
            return redirect('change_password')

    return render (request,'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    context = {
        'order_detail' : order_detail,
        'order' : order,
        'sub_total' : sub_total,

    }
    return render (request,'accounts/order_detail.html',context)

 
