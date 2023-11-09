from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('pass1')
        confirm_password=request.POST.get('pass2')
        print(email)
        print(password)
        print(confirm_password)
        if(password!=confirm_password):
            messages.warning(request,"Password is not matching")
            return render(request,'signup.html')
            
        try:
            if User.objects.get(username=email):
                messages.info(request,'Username is already taken')
                return render(request,'signup.html')
        except Exception as identifier:
            pass

        user=User.objects.create_user(email,email,password)
        # user.is_active=False
        user.save()
        messages.success(request,'Your account has been created')
        return render(request,'login.html')
    return render(request,'signup.html')    
# def signup(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['pass1']
#         confirm_password = request.POST['pass2']

#         if not email or not password or not confirm_password:
#             messages.error(request, 'Please fill in all fields')
#             return render(request, 'signup.html')

#         if password != confirm_password:
#             messages.warning(request, "Password is not matching")
#             return render(request, 'signup.html')

#         try:
#             if User.objects.get(username=email):
#                 messages.info(request, 'Username is already taken')
#                 return render(request, 'signup.html')
#         except User.DoesNotExist:
#             pass

#         user = User.objects.create_user(username=email, email=email, password=password)
#         # user.is_active = False
#         user.save()
#         messages.success(request, 'Your account has been created')
#         return render(request, 'login.html')
#     return render(request, 'signup.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('email')
        password=request.POST.get('pass1')
        myuser=authenticate(request,username=username, password=password)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('/registration/login')    
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/registration/login')    