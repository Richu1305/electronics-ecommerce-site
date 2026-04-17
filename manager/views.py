
from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,Product
from django.contrib import messages
from user.models import Order, Register

# Create your views here.
def adminhome(request):
    return render(request,'manager/adminhome.html')

def category(request):
    if request.method == 'POST':
        name = request.POST.get('Name', '').strip()
        description = request.POST.get('Description', '').strip()

        if name and description:
            Category.objects.create(Name=name, Description=description)
            messages.success(request, 'CATEGORY ADDED SUCCESSFULLY')
        else:
            messages.error(request, 'Both Category Name and Description are required.')

    return render(request, 'manager/category.html')




def view(request):
    v=Category.objects.all()
    return render(request,'manager/viewcate.html',{'data':v})


def delete(request,id):
    Category.objects.filter(id=id).delete()
    messages.success(request,'DELETED SUCCESSFULL')
    return redirect('view')
    
    
def editdata(request,id):
    e=get_object_or_404(Category,id=id)  
    if request.method == 'POST':
        e.Name=request.POST['Name']
        e.Description=request.POST['Description']
        e.save()
    r=Category.objects.filter(id=id)
    return render(request,'manager/edit.html',{'edata':r})


def add_product(request):
     c = Category.objects.all()
     if request.method == "POST":
        IMAGE = request.FILES.get('image')
        NAME = request.POST['Name']
        PRICE = request.POST['Price']
        STOCK = request.POST['Stock']
        DESCRIPTION = request.POST['Description']

        category_id = request.POST['category']   

        
        category = Category.objects.get(id=category_id)

        Product.objects.create(
            image=IMAGE,
            Name=NAME,
            Price=PRICE,
            stock=STOCK,
            category=category,   
            Description=DESCRIPTION
        )

     return render(request, 'manager/add_product.html',{'c':c})
    


def view_product(request):
    viewproduct=Product.objects.all()
    return render(request,'manager/view_product.html',{'data':viewproduct})


def delete_product(request, id):
    Product.objects.filter(id=id).delete()
    messages.success(request,'DELETED SUCCESSFULL')
    return redirect('view_product')
    
    
def edit_prodct(request,id):
    c=Category.objects.all() 
    p=get_object_or_404(Product,id=id)  
    if request.method == 'POST':
        p.Name=request.POST['Name']
        p.Price=request.POST['price']
        p.stock=request.POST['stock']
        p.category_id=request.POST['category']
        if 'description' in request.POST:
            p.Description=request.POST['description']
        if 'image' in request.FILES:
            p.image=request.FILES['image']
        p.save()
    editproduct=Product.objects.filter(id=id)
    
    return render(request,'manager/editproduct.html',{'pdata':editproduct,'c':c})

def cancel_order(request, id):
    order = get_object_or_404(Order, id=id)

    order.orderstatus = 'Canceled'
    order.paymentstatus = 'Failed'
    order.save()

    return redirect('userorder')

def Completeorder(request,id):
    order=get_object_or_404(Order,id=id)
    order.orderstatus='Completed'
    order.paymentstatus='Completed'
    order.save()
    return redirect('userorder')

def userorder(request):
    status=request.GET.get('status')
    orders = Order.objects.all()
    if status == 'pending':
        orders=Order.objects.filter(orderstatus='pending')
    if status == 'Processing':
        orders=Order.objects.filter(orderstatus='Processing')
    if status == 'Completed':
        orders=Order.objects.filter(orderstatus='Completed')
    if status =='Canceled':
        orders=Order.objects.filter(orderstatus='Canceled')
    if status =='all':
        orders=Order.objects.all()
    
    
    users = Register.objects.all()
    return render(request,'manager/userorder.html',{'orders':orders,'users': users})



def orderdetails_for_manager(request,id):
    order=get_object_or_404(Order,id=id)
    if request.method == "POST":
        if 'start_processing' in request.POST:
            order.deliverydate=request.POST['delivery_date']
            order.carrier=request.POST['carrier']
            order.tracking_id=request.POST['tracking_id']
            order.orderstatus='Processing'
            order.save()
        if 'cancel' in request.POST:
            order.orderstatus='Canceled'
            order.paymentstatus='Failed'
            order.save()
        

    return render(request,'manager/orderdetails.html',{'order':order})

