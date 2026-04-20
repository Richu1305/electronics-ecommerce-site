from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from .models import Register, Cart, Cartitems, Order, orderitem, Wishlist, review
from manager.models import Product,Category
from django.contrib import messages
from django.contrib.auth import authenticate,login,get_user_model
import datetime
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
import stripe


stripe.api_key=settings.STRIPE_SECRET_KEY




# Create your views here.
def home(request):
    return render(request,'common/base.html')


def form(request):
    if request.method == 'POST':

        PROFILE = request.FILES.get('profile')
        FIRSTNAME = request.POST['Firstname']
        LASTNAME = request.POST['Lastname']
        USERNAME = request.POST['Username']
        EMAIL = request.POST['Email']
        password = request.POST['Password']
        ADDRESS = request.POST.get('Address')
        CITY = request.POST['City']
        STATE = request.POST['State']
        PHONE = request.POST['Phone']
        POSTAL_CODE = request.POST['Postal_code']

      
        if User.objects.filter(username=USERNAME).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'common/form.html')

        
        if User.objects.filter(email=EMAIL).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'common/form.html')

        
        u = User.objects.create_user(
            first_name=FIRSTNAME,
            last_name=LASTNAME,
            username=USERNAME,
            password=password,
            email=EMAIL
        )
        u.save()

        customer = Register.objects.create(
            user=u,
            address=ADDRESS,
            phone=PHONE,
            postal_code=POSTAL_CODE,
            city=CITY,
            state=STATE,
            profile_photo=PROFILE
        )

        customer_obj, create = Group.objects.get_or_create(name='CUSTOMER')
        customer_obj.user_set.add(u)

        messages.success(request, 'Registration was successful..')

    return render(request, 'common/form.html')

def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.groups.filter(name='CUSTOMER').exists():
                login(request,user)
                return redirect('userhome')
            else:
                return redirect('adminhome')
        else:
            messages.error(request,'Invalid username or password!')
            

    return render(request,'common/login.html')
    
        

def userhome(request):
    data = Product.objects.all()
    c = Category.objects.all()
   
    search = request.GET.get('search')
    category = request.GET.get('category')

    if search:
        search_clean = search.strip().lower()
        from django.db.models import Q
        if search_clean in ['appliances', 'appliance']:
            data = data.filter(
                Q(category__Name__icontains=search) |
                Q(Name__icontains=search) |
                Q(category__Name__icontains='Refrigerator') |
                Q(Name__icontains='Refrigerator') |
                Q(category__Name__icontains='Washing Machine') |
                Q(Name__icontains='Washing Machine') |
                Q(category__Name__icontains='Air Conditioner') |
                Q(Name__icontains='Air Conditioner') |
                Q(category__Name__icontains='Microwave Oven') |
                Q(Name__icontains='Microwave Oven') |
                Q(category__Name__icontains='Water Purifier') |
                Q(Name__icontains='Water Purifier')
            )
        elif search_clean in ['mobile', 'mobiles']:
            data = data.filter(
                Q(category__Name__icontains=search) |
                Q(Name__icontains=search) |
                Q(category__Name__icontains='Tablet') |
                Q(Name__icontains='Tablet') |
                Q(category__Name__icontains='Watch') |
                Q(Name__icontains='Watch') |
                Q(category__Name__icontains='Earphones') |
                Q(Name__icontains='Earphones') |
                Q(category__Name__icontains='Power Bank') |
                Q(Name__icontains='Power Bank') |
                Q(category__Name__icontains='Controller') |
                Q(Name__icontains='Controller')
            )
        elif search_clean in ['electronics', 'electronic']:
            data = data.filter(
                Q(category__Name__icontains=search) |
                Q(Name__icontains=search) |
                Q(category__Name__icontains='Laptop') |
                Q(Name__icontains='Laptop') |
                Q(category__Name__icontains='Printer') |
                Q(Name__icontains='Printer') |
                Q(category__Name__icontains='Projector') |
                Q(Name__icontains='Projector') |
                Q(category__Name__icontains='Speaker') |
                Q(Name__icontains='Speaker') |
                Q(category__Name__icontains='Keyboard') |
                Q(Name__icontains='Keyboard') |
                Q(category__Name__icontains='Mouse') |
                Q(Name__icontains='Mouse') |
                Q(category__Name__icontains='Monitor') |
                Q(Name__icontains='Monitor') |
                Q(category__Name__icontains='External Hard Drive') |
                Q(Name__icontains='External Hard Drive') |
                Q(category__Name__icontains='USB Flash Drive') |
                Q(Name__icontains='USB Flash Drive') |
                Q(category__Name__icontains='Game Controller') |
                Q(Name__icontains='Game Controller') |
                Q(category__Name__icontains='Camera') |
                Q(Name__icontains='Camera')
            )
        elif search_clean == 'for you':
            pass  # Do not filter, to display all products
        else:
            data = data.filter(Q(Name__icontains=search) | Q(category__Name__icontains=search))

    if category:
        data = data.filter(category_id=category)
        
    if request.user.is_authenticated:
        w = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        w = []

    return render(request, 'user/userhome.html', {'data': data,'c': c,'w':w})

def productdetails(request, id):
    product = get_object_or_404(Product, id=id)
    r=review.objects.filter(product=product)
    return render(request, 'user/productdetails.html', {'product': product,'r':r})

def addtocart(request,id):
    if request.method == "POST":
        product = get_object_or_404(Product,id=id)
        quantity=int(request.POST.get('quantity',1))
        is_buy_now = request.POST.get('buy_now')
        
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item,created = Cartitems.objects.get_or_create(cart=cart,product=product,defaults={'quantity':quantity})
        

        if not created:
            new_quantity=cart_item.quantity+quantity
            if new_quantity<=product.stock:
                cart_item.quantity=new_quantity
            else:
                cart_item.quantity=product.stock
        cart_item.save()
          
        if is_buy_now == 'true':
            request.session['buy_now_item'] = cart_item.id
            return redirect('checkout')

    return redirect('cartitems')

def cartitems(request):
    if 'buy_now_item' in request.session:
        del request.session['buy_now_item']
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = Cartitems.objects.filter(cart=cart)

    grand_total = 0

    for item in items:
        item.total = item.product.Price * item.quantity
        grand_total += item.total

    return render(request, 'user/cart.html', {
        'items': items,
        'grand_total': grand_total
    })
    


def increasequantity(request,id):
    item=get_object_or_404(Cartitems,id=id)
    if item.quantity<item.product.stock:
        item.quantity+=1
        item.save()
    else:
        messages.error(request,'Out of Stock')
    return redirect('cartitems')


def decreasequantity(request,id):
    item=get_object_or_404(Cartitems,id=id)
    if item.quantity<item.product.stock:
        item.quantity-=1
        item.save()
    if item.quantity == 0:
           item.delete()
    return redirect('cartitems')

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    buy_now_item_id = request.session.get('buy_now_item')
    
    if buy_now_item_id:
        items = Cartitems.objects.filter(cart=cart, id=buy_now_item_id)
    else:
        items = Cartitems.objects.filter(cart=cart)

        
    grand_total = 0

    for item in items:
        item.total = item.product.Price * item.quantity
        grand_total += item.total
    
    

    return render(request,'user/checkout.html',{'items':items,'grand_total': grand_total})



def cash_on_delivery(request):
    cart=Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('cartitems')
    
    buy_now_item_id = request.session.get('buy_now_item')
    if buy_now_item_id:
        cart_items=Cartitems.objects.filter(cart=cart, id=buy_now_item_id)
    else:
        cart_items=Cartitems.objects.filter(cart=cart)
        
    total=0
    for item in cart_items:
        total += item.product.Price*item.quantity
    order=Order.objects.create(
        user=request.user,
        orderdate=datetime.datetime.now(),
        paymentstatus='Pending',
        payment_method='COD',
        total_amount=total
        
    )
    for item in cart_items:
        orderitem.objects.create(
            order=order,
            product=item.product,
            price=item.product.Price,
            quantity=item.quantity
        )
        item.product.stock -= item.quantity
        item.product.save()
    cart_items.delete()

    if 'buy_now_item' in request.session:
        del request.session['buy_now_item']

    return redirect('ordersuccess',order.id)





def upi(request):
    cart=Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('cartitems')
        
    buy_now_item_id = request.session.get('buy_now_item')
    if buy_now_item_id:
        cart_items=Cartitems.objects.filter(cart=cart, id=buy_now_item_id)
    else:
        cart_items=Cartitems.objects.filter(cart=cart)
        
    if not cart_items.exists():
        return redirect('cartitems')
    
    line_items=[]
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.product.Name,
                },
                'unit_amount': int(item.product.Price * 100),
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/payment_success',   
        cancel_url='http://127.0.0.1:8000/viewcart',
    )

    return redirect(session.url)


def payment_success(request):
    cart=Cart.objects.filter(user=request.user).first()
    if not cart:
        return redirect('cartitems')
        
    buy_now_item_id = request.session.get('buy_now_item')
    if buy_now_item_id:
        cart_items=Cartitems.objects.filter(cart=cart, id=buy_now_item_id)
    else:
        cart_items=Cartitems.objects.filter(cart=cart)
        
    total=0
    for item in cart_items:
        total += item.product.Price*item.quantity
    order=Order.objects.create(
        user=request.user,
        orderdate=datetime.datetime.now(),
        paymentstatus='Paid',
        payment_method='UPI',
        total_amount=total
        
    )
    for item in cart_items:
        orderitem.objects.create(
            order=order,
            product=item.product,
            price=item.product.Price,
            quantity=item.quantity
        )
        item.product.stock -= item.quantity
        item.product.save()
    cart_items.delete()

    if 'buy_now_item' in request.session:
        del request.session['buy_now_item']

    return redirect('ordersuccess',order.id)

     
    


def ordersuccess(request,id):
    o=get_object_or_404(Order,id=id)
    return render(request,'user/ordersuccess.html',{'order':o})

def vieworder(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your orders.')
        return redirect('login_user')

    orders = orderitem.objects.filter(order__user=request.user)
    
    grand_total = 0

    for item in orders:
        item.total = item.product.Price * item.quantity
        grand_total += item.total
    return render(request,'user/vieworder.html',{'orders':orders,'grand_total': grand_total})

def orderdetails(request,id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view order details.')
        return redirect('login_user')

    order = Order.objects.get(id=id)
    items = orderitem.objects.filter(order=order)

    return render(request,'user/orderdetails.html',{'order':order,'items':items}) 

def userdetails(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your profile.')
        return redirect('login_user')

    user_details=Register.objects.get(user=request.user)
    return render(request,'user/userdetails.html',{'user_details':user_details})

def edituser(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to edit your profile.')
        return redirect('login_user')

    user_details= Register.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get('profile_photo'):
            user_details.profile_photo = request.FILES.get('profile_photo')
        user_details.user.first_name = request.POST['first_name']
        user_details.user.last_name = request.POST.get('last_name')
        user_details.user.username=request.POST.get('username')
        user_details.user.email = request.POST.get('email')
        user_details.phone = request.POST.get('phone')
        user_details.address = request.POST.get('address')
        user_details.city = request.POST.get('city')
        user_details.state = request.POST.get('state')
        user_details.postal_code = request.POST.get('postal_code')
        user_details.save()
        user_details.user.save()
        return redirect('userdetails')
    return render(request,'user/edituser.html',{'user_details':user_details})
    

def generate_token():
     return get_random_string(20)

def password_reset_request(request):
    if request.method == "POST":
         email = request.POST.get('email')
         try:
             user = User.objects.get(email=email)
         except User.DoesNotExist:
             messages.error(request, "User with this email does not exist.")
             return redirect('password_reset_request')

         token =default_token_generator.make_token(user)
         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
         reset_url = request.build_absolute_uri(reverse('password_reset_confirm',kwargs={'uidb64':uidb64,'token':token}))
         subject = "Password Reset Request"
         message = render_to_string('common/password_reset_email.html', {
             'user': user,
             'reset_url': reset_url,
         })
         try:
             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=message)
             messages.success(request, "A password reset link has been sent to your email.")
         except Exception as e:
             messages.error(request, f"Failed to send email: {e}")
         return redirect('login_user')
    return render(request,'common/password_reset_form.html')

def password_reset_confirm(request, uidb64, token):
        User=get_user_model()
        try:
          uid = force_str(urlsafe_base64_decode(uidb64))
          user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            print(user)
        if user is not None and default_token_generator.check_token(user,token):
             if request.method == 'POST':
                  password1=request.POST.get('password1')
                  password2=request.POST.get('password2')

                  if password1 == password2:
                      user.password = make_password(password1)
                      user.save()
                      messages.success(request,'your password has been reset')
                      return redirect('login_user')
                  else:
                      messages.error(request,'password do not match')
                      return render(request,'common/password_reset_confirm.html')
                          
             return render(request,'common/password_reset_confirm.html')
        else:
           messages.error(request, 'Invalid or expired token')
           return redirect('password_reset_request')
       
       
       
       
def add_to_wishlist(request,id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to add items to your wishlist.')
        return redirect('login_user')

    product=Product.objects.get(id=id)
    wishlist_item=Wishlist.objects.filter(
        user=request.user,
        product=product
    ).first()
    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            user=request.user,
            product=product
        )
    return redirect('userhome')

def wishlist(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your wishlist.')
        return redirect('login_user')

    w = Wishlist.objects.filter(user=request.user)
    return render(request, 'user/wishlist.html', {'w': w})

def add_review(request,id):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        rating=request.POST.get('rating')
        product=Product.objects.get(id=id)
        
        review.objects.create(
            user=request.user,
            product=product,
            comment=comment,
            rating=rating
            
        )
    return redirect('productdetails',id)





def logout(request):
        if request.user.is_authenticated:
            request.session.flush()
        return redirect('home')


