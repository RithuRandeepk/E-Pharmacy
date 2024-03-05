from django.shortcuts import render, redirect
import razorpay
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.generic import View,TemplateView,DetailView
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from app1.models import UserRegisterModel,Payment
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .models import UploadedFilemodel,Products,Categories,Cart,Customer,OrderPlaced,Wishlist,Payment
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import CustomerProfileform
from django.contrib.auth.forms import PasswordChangeForm
from app1.forms import MyPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from django.utils.decorators import method_decorator


def home(request):

    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))

    return render(request,'home.html')


def about(request):

    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')


# @method_decorator(login_required,name='dispatch')
class HomeView(TemplateView):
    template_name="home2.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # totalitem=0
        # wishitem=0
        # if request.user.is_authenticated:
        #     totalitem=len(Cart.objects.filter(user=request.user))
        #     wishitem=len(Wishlist.objects.filter(user=request.user))
          
        all_products = Products.objects.all()
      
        context["Products"] = all_products
        # context["totalitem"] = totalitem  # Add totalitem to the context
        return context


class Registration(View):
    
    def get(self,request,*args,**kwargs):
       

        return render(request,'home.html')

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            username = request.POST.get('uname')
            email = request.POST.get('email')
            phone = request.POST.get('phno')
            passw = request.POST.get('pass1')
            cnpassword = request.POST.get('pass2')


            if UserRegisterModel.objects.filter(email=email).exists():

                # messages.warning(request, "Email Already exist")
                # return redirect('homepage')
            

            
                url = '/'
                resp_body = '<script>alert("Email already exist!");\
                                                    window.location="%s"</script>' % url
                return HttpResponse(resp_body)
            
            
            if UserRegisterModel.objects.filter(phone=phone).exists():

                # messages.warning(request, "Phone Number Already exist")
                # return redirect('ipage')
            

                url = '/'
                resp_body = '<script>alert("Phone Number already exist!");\
                                                    window.location="%s"</script>' % url
                return HttpResponse(resp_body)


           
            if passw != cnpassword:

                # messages.warning(request, "Password Mismatch")
                # return redirect('homeipage')
            


                url = '/'
                resp_body = '<script>alert("Phone Number already exist!");\
                                                    window.location="%s"</script>' % url
                return HttpResponse(resp_body)
            

           
            UserRegisterModel.objects.create(first_name=username,username=email,email=email,phone=phone,password=make_password(passw),usertype="user")

            # messages.success(request, 'Registration Succesfull.')
            return redirect('loginpage')

            url = '/'
            resp_body = '<script>alert("Registration Succesful!");\
                                                    window.location="%s"</script>' % url
 
            return HttpResponse(resp_body)
class LoginView(View):
    
    def get(self, request):

        return render(request,'loginpage.html') 
    
     
    def post(self,request):
         

        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)
        print(password)
        
        try:
            usr =  UserRegisterModel.objects.get(email=email)
         
        except :
            usr = None
        
        # print(usr)

        if(usr):
            print('email exists')
            
            user = authenticate(username=usr.email,password=password)
            # print(user)
            
            print("user",user)
            if user:
                usertype = user.usertype

                if usertype == "admin":
                
                    login(request, user)
                    
                    return render(request,'home2.html')
                    
                

                elif usertype == "user":
                    
                    print('user_id',usr.id)
                    login(request, user)
                    
                     
                   
                    return redirect('home2')


                else:
                        messages.warning(request, "Unkonown user type")
                        # return HttpResponse('Unknown user type')
            else:

                # url = '/'
                # resp_body = '<script>alert("Wrong password...");\
                #                                                 window.location="%s"</script>' % url
                # return HttpResponse(resp_body)


                messages.warning(request, "Wrong password")
                return redirect('loginpage')

                
        else:


            url = '/'
            resp_body = '<script>alert("Invalid user...");\
                                                            window.location="%s"</script>' % url
            return HttpResponse(resp_body)



def upload_file(request):
     
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        uploaded_by = request.user
        new_upload = UploadedFilemodel(file=uploaded_file, uploaded_by=uploaded_by, uploaded_at=timezone.now())
        new_upload.save()
        # return HttpResponse('File uploaded successfully.')
        url = '/'
        resp_body = '<script>alert("Uploaded...We will contact you soon..");\
                                                            window.location="%s"</script>' % url
        return HttpResponse(resp_body)
        return render(request,'home2.html')



class ProductView(View):
    def get (self,request,val):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        
    
       
        category_object = Categories.objects.get(category_name=val)
        product= Products.objects.filter(category=category_object)
        product_name= Products.objects.filter(category=category_object).values('product_name')
        brand=Products.objects.filter(category=category_object).values('brand').distinct()
        return render(request,'productview.html',locals())
    



class Productdetail(View):
    def get (self,request,pk):

        # pk = int(pk)
        product = get_object_or_404(Products, pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
        
              
        return render(request,'productdetail.html',locals())
    
class BrandwiseDisplay(View):

    def get(self,request,val):

        product= Products.objects.filter(brand=val)
        product_name=Products.objects.filter(brand=val).values('product_name')
 
        return render(request,'productview.html',locals())

def add_to_cart(request):
    user=request.user
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    product_id=request.GET.get('prod_id')
    totalitem=0
    if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
    product=Products.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('cart')


def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    amount=0
    for p in cart:
        value=p.quantity*p.product.selling_price
        amount=amount+value
    totalamount=amount+40
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'addtocart.html',locals())


class ProfileView(View):
    def get(self,request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        
        return render(request,'profile.html',locals())
    
    
    def post(self,request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        form=CustomerProfileform(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            housename=form.cleaned_data['housename']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,housename=housename,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Profile saved succesfully")
        # else:
        #     messages.warning(request,'invalid input data')
        return render(request,'profile.html',locals())
    

def address(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())


class Updateaddress(View):
    def get(self,request,pk):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        

        add=Customer.objects.get(pk=pk)
        form=CustomerProfileform(instance=add)
        return render(request,'updateaddress.html',locals())
    
    def post(self,request,pk):
        form=CustomerProfileform(request.POST)
        if form.is_valid():

            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.housename=form.cleaned_data['housename']
            add.locality=form.cleaned_data['locality']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.zipcode=form.cleaned_data['zipcode']
            add.save()

         
            messages.success(request,"Profile Updated succesfully")
        else:
            messages.warning('request','invalid inputdata')
      
        return redirect('address')
    

def add_to_cart(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Products.objects.get(id=product_id)
    quantity = int(request.GET.get('quantity', 1))
    Cart(user=user,product=product,quantity=quantity).save()
    return redirect('/cart')




def show_cart(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0

    for p in cart:
        if p.quantity is not None and p.product is not None and p.product.selling_price is not None:
            value = p.quantity * p.product.selling_price
            amount += value
        else:
        
            pass

    totalamount = amount + 40
    return render(request, 'addtocart.html',locals())



def plus_cart(request):

    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.selling_price
            amount=amount+value
        totalamount=amount+40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)



def minus_cart(request):

    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.selling_price
            amount=amount+value
        totalamount=amount+40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)


def remove_cart(request):

    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        c.delete()
     
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.selling_price
            amount=amount+value
        totalamount=amount+40
        data={
           
            'amount':amount,
            'totalamount':totalamount

        }
        return JsonResponse(data)
    

class checkout(View):
    def get(self,request):
        totalitem=0
        wishitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount=0
        for p in cart_items:
            value= p.quantity * p.product.selling_price
            famount=famount+value
        totalamount=famount+40
        razoramount=int(totalamount * 100)
        client=razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data={"amount":razoramount,'currency':'INR','receipt':'order_rcptid_12'}
        payment_response=client.order.create(data=data)
        print(payment_response)
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status == 'created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status

            )
            payment.save()

        return render(request,'checkout.html',locals())


def payment_done(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        

    order_id=request.GET.get('order_id')
    Payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=Payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')
    


# def payment_done(request):
#     totalitem = 0
#     wishitem = 0

#     if request.user.is_authenticated:
#         totalitem = Cart.objects.filter(user=request.user).count()
#         wishitem = Wishlist.objects.filter(user=request.user).count()

#     order_id = request.GET.get('order_id')
#     payment_id = request.GET.get('payment_id')
#     cust_id = request.GET.get('cust_id')

#     # Check if cust_id is a valid integer before querying the database
#     try:
#         cust_id = int(cust_id)
#     except (TypeError, ValueError):
#         # Handle the case where cust_id is not a valid integer
#         # You might want to add proper error handling or redirect the user to an error page
#         return redirect('error_page')

#     # Use get_object_or_404 to handle the case where the customer is not found
#     customer = get_object_or_404(Customer, id=cust_id)
#     payment = get_object_or_404(Payment, razorpay_order_id=order_id)

#     # Update payment details
#     payment.paid = True
#     payment.razorpay_payment_id = payment_id
#     payment.save()

#     # Process cart items and create orders
#     user = request.user
#     cart_items = Cart.objects.filter(user=user)

#     for cart_item in cart_items:
#         OrderPlaced.objects.create(
#             user=user,
#             customer=customer,
#             product=cart_item.product,
#             quantity=cart_item.quantity,
#             payment=payment
#         )
#         cart_item.delete()

#     return redirect('orders')



def orders(request):
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request,'orders.html',locals())

@login_required
def plus_wishlist(request):

    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        prod_id=int(prod_id)
    
        product = Products.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':' Added to Wishlist'
        }

        return JsonResponse(data)
        
@login_required
def minus_wishlist(request):

    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        prod_id=int(prod_id)
    
        product = Products.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'Deleted from Wishlist'
        }

        return JsonResponse(data)
    

def search(request):

    query=request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=Cart.objects.filter(user=request.user).count()
        wishitem=Wishlist.objects.filter(user=request.user).count()
    product = Products.objects.filter(Q(product_name__icontains=query.strip()))
    return render(request, 'search.html', {'query': query, 'totalitem': totalitem, 'wishitem': wishitem, 'product': product})



def show_wishlist(request):
    user=request.user
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishitem=len(Wishlist.objects.filter(user=request.user))
        product=Wishlist.objects.filter(user=user)
        return render(request,'Wishlist.html',locals())








