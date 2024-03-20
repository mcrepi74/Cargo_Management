from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from users.models import User
from cargo_app.models import CorporateUser, Shipment
from IPython import embed

def edituser(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id=pk)
        return render(request, 'users/edituser.html', {'userid': request.COOKIES['userid'], 'user': user})
    elif request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exists():
            return render(request, "users/edituser.html", {'userid': request.COOKIES['userid'], 'message': 'Email has already been used.', 'messagetype': 2})
        User.objects.filter(id=pk).update(name=params["uname"], surname=params["sname"], password=params["passwd"], telephone=params["telno"], email=params["mail"])
        return render(request, "home/home.html", {'userid': request.COOKIES['userid'], 'message': 'User information has been changed', 'messagetype': 1})

def adduser(request):
    if request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exists():
            return render(request, "users/adduser.html", {'userid': request.COOKIES['userid'], 'message': 'Email has already been used.', 'messagetype': 2})
        User.objects.create(name=params["uname"], surname=params["sname"], password=params["passwd"], telephone=params["telno"], email=params["mail"])
        return render(request, "home/home.html", {'userid': request.COOKIES['userid'], 'message': 'A new User Created', 'messagetype': 1})
    elif request.method == 'GET':
        return render(request, "users/adduser.html", {'userid': request.COOKIES['userid']})

def register(request):
    if request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exists():
            return render(request, "users/register.html", {'firms': CorporateUser.objects.all(), 'message': 'Email has already been used.', 'messagetype': 2})
        User.objects.create(name=params["uname"], surname=params["sname"], password=params["passwd"], telephone=params["telno"], email=params["mail"])
        return render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'message': 'You are registered', 'messagetype': 1})
    elif request.method == 'GET':
        return render(request, "users/register.html")

def login(request):
    if 'userid' in request.COOKIES:
        return render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'message': 'Already login', 'messagetype': 2})
    if request.method == 'POST':
        params = request.POST
        filtered_query = User.objects.filter(email=params['mail'])
        if filtered_query.exists() and filtered_query[0].password == params['passwd']:
            response = render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'userid': filtered_query[0].id, 'message': 'Successful Login', 'messagetype': 1})
            response.set_cookie('userid', filtered_query[0].id)
            return response
        else:
            return render(request, "users/login.html", {'message': 'Invalid email or password', 'messagetype': 2})
    elif request.method == 'GET':
        return render(request, "users/login.html")

def details(request, pk):
    try:
        user = User.objects.get(pk=pk)  # Récupérer l'utilisateur avec l'ID spécifié
    except User.DoesNotExist:  # Gérer le cas où l'utilisateur n'existe pas
        return HttpResponse("User does not exist", status=404)
    
    if request.method == 'GET':
        return render(request, "users/details.html", {'userid': request.COOKIES.get('userid'), 'User': user})
    elif request.method == 'POST':
        params = request.POST
        user.name = params.get('uname')
        user.surname = params.get('sname')
        user.password = params.get('passwd')
        user.email = params.get('mail')
        user.telephone = params.get('telno')
        user.save()
        return render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'userid': request.COOKIES.get('userid'), 'message': 'Changes Saved', 'messagetype': 1})

def user_logout(request):  # Nouvelle vue pour gérer la déconnexion
    if 'userid' in request.COOKIES:
        response = render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'message': 'Successful Logout', 'messagetype': 1})
        response.delete_cookie('userid')
        return response
    else:
        return redirect('login')  # Redirige vers la page de connexion si l'utilisateur n'est pas connecté

def delete(request, pk):
    if request.COOKIES['userid'] != pk:
        User.objects.filter(id=pk).delete()
    return render(request, 'adminpanel/index.html', {'userid': request.COOKIES['userid'], 'shipmentList': list(Shipment.objects.all()), 'userList': list(User.objects.all())})

def update(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id=pk)
        return render(request, 'users/profile.html', {'userid': request.COOKIES['userid'], 'user': user})
    if request.method == 'POST':
        params = request.POST
        if User.objects.filter(email=params["mail"]).exists():
            return render(request, "users/profile.html", {'message': 'Email has already been used.', 'messagetype': 2})
        User.objects.filter(id=pk).update(name=params["uname"], surname=params["sname"], password=params["passwd"], telephone=params["telno"], email=params["mail"])
        return render(request, "home/home.html", {'firms': CorporateUser.objects.all(), 'userid': request.COOKIES['userid'], 'message': 'User information has been changed', 'messagetype': 1})

def makeadmin(request, pk):
    User.objects.filter(id=pk).update(isAdmin=True)
    return render(request, 'adminpanel/index.html', {'userid': request.COOKIES['userid'], 'shipmentList': list(Shipment.objects.all()), 'userList': list(User.objects.all())})
