from django.shortcuts import render, HttpResponseRedirect
from main.models import Event

# Create your views here

def index(request):
	return render(request, 'add_event/event.html')

def submit(request):
	if ('name' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter an event name'}
		return render(request, 'add_event/message.html', context)
	else:
		name = request.POST['name']

	if ('fee' not in request.POST):
		context = {'message1':'Error', 'message2':'Please enter the event registration fee'}
		return render(request, 'add_event/message.html', context)
	else:
		fee = request.POST['fee'];

	if ('teamFee' in request.POST):
		teamFee = request.POST['teamFee']
	else:
		teamFee = None

	if ('minimum' in request.POST):
		minimum = request.POST['minimum']
	else:
		minimum = None

	if ('maximum' in request.POST):
		maximum = request.POST['maximum']
	else:
		maximum = None

	data = Event(name=name, minimum=minimum, maximum=maximum, fee=fee, team=teamFee)
	data.save()

	context = {'redirect':'true'}
	return render(request, 'add_event/event.html', context)