from django.shortcuts import render, HttpResponse
from main.models import Participent

# Create your views here.

def index(request):
	return render(request, 'register/register_user.html')

def submit(request):
	if('name' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the participent name', 'message3':'/register/', 'message4':'%'}
		return render(request, 'register/message.html', context)

	if('college' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the college name', 'message3':'/register/', 'message4':'%'}
		return render(request, 'register/message.html', context)	

	if('email' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the participent email id', 'message3':'/register/', 'message4':'%'}
		return render(request, 'register/message.html', context)

	if('phone' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the participent phone number', 'message3':'/register/', 'message4':'%'}
		return render(request, 'register/message.html', context)

	if('gender' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the participent gender', 'message3':'/register/', 'message4':'%'}
		return render(request, 'register/message.html', context)

	if('dob' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the participent DOB', 'message3':'/register/', 'message4':'%'}
		return render(request, 'register/message.html', context)

	try:
		data = Participent.objects.get(phone_no=request.POST['phone'])
	except Participent.DoesNotExist:
		row = Participent(name=request.POST['name'], institution=request.POST['college'], email=request.POST['email'], phone_no=request.POST['phone'], gender=request.POST['gender'], dob=request.POST['dob'])
		row.save()
		context={'message1':'Success', 'message2':'Successfully registered!!\n Your participant id is CAW{}'.format(row.id)}
		return render(request, 'register/message.html', context)
	else:
		context={'message1':'Error', 'message2':'Participant with a similar phone number already exists'}
		return render(request, 'register/message.html', context)