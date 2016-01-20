from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		if('loc' not in request.GET):
			context ={'message1':'Message', 'message2':'You have already logged in'}
			return render(request, 'login/message.html', context)
		else:
			if(request.GET['loc'] == 'add_event'):
				return HttpResponseRedirect(redirect_to='/add_event/')
	else:
		if('loc' not in request.GET):
			return render(request, 'login/login.html')
		else:
			if(request.GET['loc'] == 'add_event'):
				context = {'redirect_location':'add_event'}
				return render(request, 'login/login.html', context)

def submit(request):
	if request.user.is_authenticated():
		if('loc' not in request.GET):
			context ={'message1':'Message', 'message2':'You have already logged in'}
			return render(request, 'login/message.html', context)
		else:
			if(request.GET['loc'] == 'add_event'):
				return HttpResponseRedirect(redirect_to='/add_event/')
	else:
		if('un' not in request.POST):
			context ={'message1':'Message', 'message2':'You have already logged in', 'message3':'/login/', 'message4':'#'}
			return render(request, 'login/message.html', context)
		if('pw' not in request.POST):
			context ={'message1':'Message', 'message2':'You have already logged in', 'message3':'/login/', 'message4':'#'}
			return render(request, 'login/message.html', context)
		user = authenticate(username=request.POST['un'], password=request.POST['pw'])
		if user is not None:
			login(request, user)
			if('loc' not in request.GET):
				context ={'message1':'Message', 'message2':'You have successfully logged in'}
				return render(request, 'login/message.html', context)
			else:
				if(request.GET['loc'] == 'add_event'):
					return HttpResponseRedirect(redirect_to='/add_event/')	
		else:
			context ={'message1':'Message', 'message2':'Username password combo doesnt match', 'message3':'/login/', 'message4':'#'}
			return render(request, 'login/message.html', context)

def lo(request):
	if request.user.is_authenticated():
		logout(request)
		context ={'message1':'Message', 'message2':'You have successfully logged out'}
		return render(request, 'login/message.html', context)
	else:
		context ={'message1':'Message', 'message2':'Please login first'}
		return render(request, 'login/message.html', context)

def default(request):
	return render(request, 'login/home.html')
