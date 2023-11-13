from django.shortcuts import render,redirect
from .models import Contact,Product, Orders, OrderUpdate
from django.contrib import messages
from math import ceil

# Create your views here.
def index(request):
    allProds=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n//4+ceil(n/4)-(n//4)
        allProds.append([prod,range(1,nSlides),nSlides])
    context={'allProds':allProds}    
    return render(request,'index.html',context)

def contact(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        phonenumber=request.POST.get('phonenumber')
        myquery=Contact(name=name, email=email, desc=desc, phonenumber=phonenumber)
        myquery.save()
        messages.info(request,'We will back to you soon...')
        return render(request,'contact.html')
    return render(request,'contact.html')    

def checkout(request):
    return render(request,'confirmation.html')


def checkout(request):
     if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/registration/login')
     if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
        messages.success(request,'Thankyou for shopping . Your order has been placed')
        # # PAYMENT INTEGRATION

        # id = Order.order_id
        # oid=str(id)+"ShopyCart"
        # param_dict = {

        #     'MID':keys.MID,
        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'WEBSITE': 'WEBSTAGING',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',

        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # return render(request, 'paytm.html', {'param_dict': param_dict})

     return render(request, 'checkout.html')

def about(request):
    return render(request,'about.html')  


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/registration/login')
    currentuser=request.user.username
    items=Orders.objects.filter(email=currentuser)
    for i in items:
        print(i.name)
    #     status=OrderUpdate.objects.filter(order_id=int(myid))
    # for j in status:
    #     print(j.update_desc)

   
    context ={"items":items,}
    # print(currentuser)
    return render(request,"profile.html",context)     
