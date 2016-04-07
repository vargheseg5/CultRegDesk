from django.shortcuts import render, HttpResponseRedirect
from main.models import Event
from django.contrib.auth.decorators import login_required

# Create your views here

@login_required(login_url='/login/?loc=add_event')
def index(request):
	return render(request, 'add_event/event.html')

@login_required(login_url='/login/?loc=add_event')
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

	tf = None
	if ('teamFee' in request.POST):
		teamFee = request.POST['teamFee']
		if teamFee == 'true':
			tf = True
		else:
			tf = False
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

	if maximum is None and minimum is None:
		data = Event(name=name, minimum=minimum, maximum=maximum, fee=fee, team=False, teamCollect=tf, registration_active=True)
	else:
		data = Event(name=name, minimum=minimum, maximum=maximum, fee=fee, team=True, teamCollect=tf, registration_active=True)
	data.save()

	context = {'redirect':'true'}
	return render(request, 'add_event/event.html', context)