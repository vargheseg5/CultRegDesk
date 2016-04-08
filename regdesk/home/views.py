from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main.models import Event, Participent, Participation, Registration
from django.http import HttpResponseRedirect, StreamingHttpResponse
import csv

class Echo(object):
	def write(self, value):
		return value

@login_required(login_url='/login/?loc=home')
def index(request):
	un = request.user.first_name
	context = {'name':un}
	return render(request, 'home/reg_template.html', context)

@login_required(login_url='/login/?loc=home')
def event_registraion_1(request):
	events = Event.objects.all().order_by('name')
	context = {'events':events}
	return render(request, 'home/event_reg1.html', context)


@login_required(login_url='/login/?loc=home')
def event_registraion_2(request):
	if 'mob_no' in request.GET:
		mob_no = request.GET['mob_no']
	else:
		mob_no = None

	if 'caw_id' in request.GET:
		caw_id = request.GET['caw_id']
	else:
		caw_id = None

	if 'event' in request.GET:
		event = request.GET['event']
	else:
		context = {'message1':'Error', 'message2':'Please provide an event'}
		return render(request, 'home/message.html', context)

	if mob_no is None and caw_id is None:
		context = {'message1':'Error', 'message2':'Please provide a participent id or mobile number'}
		return render(request, 'home/message.html', context)

	if mob_no is None:
		try:
			p = Participent.objects.get(id=int(caw_id, 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'No such participent exist. Please register first'}
			return render(request, 'home/message.html', context)
	else:
		try:
			p = Participent.objects.get(phone_no=int(mob_no, 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'No such participent exist. Please register first'}
			return render(request, 'home/message.html', context)

	try:
		e = Event.objects.get(id=int(event, 10))
	except Event.DoesNotExist:
		context = {'message1':'Error', 'message2':'No such exists'}
		return render(request, 'home/message.html', context)

	if e.team == True:
		context = {'p':p, 'e':e, 'range':range(1, e.maximum+1)}
	else:
		context = {'p':p, 'e':e}
	return render(request, 'home/event_reg2.html', context)

@login_required(login_url='/login/?loc=home')
def event_registration_submit(request):
	if 'event' not in request.GET:
		context = {'message1':'Error', 'message2':'Please provide an event'}
		return render(request, 'home/message.html', context)
	else:
		e = request.GET['event']

	try:
		event = Event.objects.get(id=int(e, 10))
	except Event.DoesNotExist:
		context = {'message1':'Error', 'message2':'No such event exists'}
		return render(request, 'home/message.html', context)

	if event.registration_active == False:
		context = {'message1':'Message', 'message2':'Registration for {} has been closed by admin'.format(event.name)}
		return render(request, 'home/message.html', context)

	members = []
	if event.team == True:
		for i in range(1, (event.minimum)):
			str = 'p{}'.format(i)
			if str not in request.GET:
				context = {'message1':'Error', 'message2':'Minimum {} members must be present in the team for {}'.format(event.minimum, event.name)}
				return render(request, 'home/message.html', context)
			else:
				try:
					pa = Participent.objects.get(id=int(request.GET[str], 10))
				except Participent.DoesNotExist:
					context = {'message1':'Error', 'message2':'Team member number {} is not registered'.format(i)}
					return render(request, 'home/message.html', context)
				es = pa.participation_set.all()
				for ess in es:
					if ess.event == event:
						context = {'message1':'Error', 'message2':'Team member {} is already in a team for {}'.format(pa.name, event.name)}
						return render(request, 'home/message.html', context)
				members.append(pa)

		for i in range((event.minimum), (event.maximum)):
			str = 'p{}'.format(i)
			if str in request.GET:
				try:
					pa = Participent.objects.get(id=int(request.GET[str], 10))
				except Participent.DoesNotExist:
					try:
						pa = Participent.objects.get(phone_no=int(request.GET[str], 10))
					except Participent.DoesNotExist:
						context = {'message1':'Error', 'message2':'Team member number {} is not registered'.format(i)}
						return render(request, 'home/message.html', context)
				members.append(pa)

	if 'participent' not in request.GET:
		context = {'message1':'Error', 'message2':'Please provide the team lead details'}
		return render(request, 'home/message.html', context)
	else:
		try:
			pa = Participent.objects.get(id=int(request.GET['participent'], 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'Team kead is not registered'}
			return render(request, 'home/message.html', context)

	es = pa.participation_set.all()
	for ess in es:
		if ess.event == event:
			context = {'message1':'Error', 'message2':'Team member {} is already in a team for {}'.format(pa.name, event.name)}
			return render(request, 'home/message.html', context)

	part = Participation(event=event)
	part.save()
	part.participent.add(pa)

	for m in members:
		part.participent.add(m)

	if 'amt' in request.GET:
		amt = request.GET['amt']
	else:
		amt = 0

	r = Registration(participation=part, user=request.user, amount=amt)
	r.save()

	context = {'message1':'Success', 'message2':'Successfully registered!'}
	return render(request, 'home/message.html', context)

@login_required(login_url='/login/?loc=home')
def edit_registration_1(request):
	return render(request, 'home/edit_reg1.html')

@login_required(login_url='/login/?loc=home')
def edit_registration_2(request):
	pa = None
	if 'id' in request.GET:
		try:
			pa = Participent.objects.get(id=int(request.GET['id'], 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'No such participent exists. Register first.'}
			return render(request, 'home/message.html', context)
	elif 'mob_no' in request.GET:
		try:
			pa = Participent.objects.get(phone_no=int(request.GET['mob_no'], 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'No such participent exists. Register first.'}
			return render(request, 'home/message.html', context)
	else:
		context = {'message1':'Error', 'message2':'Please provide either a CAW id or mobile number.'}
		return render(request, 'home/message.html', context)


	events = pa.participation_set.all()
	if 'confirm' in request.GET:
		context = {'events':events, 'id':pa.id, 'confirm':'t'}
	else:
		context = {'events':events, 'id':pa.id}
	return render(request, 'home/edit_reg2.html', context)

@login_required(login_url='/login/?loc=home')
def delete_registration(request):
	if 'id' in request.GET:
		i = request.GET['id']
	else:
		context = {'message1':'Error', 'message2':'Please specify the event to be deleted.'}
		return render(request, 'home/message.html', context)

	if 'pa' in request.GET:
		p = request.GET['pa']
	else:
		context = {'message1':'Error', 'message2':'Please specify the participent.'}
		return render(request, 'home/message.html', context)

	try:
		part = Participation.objects.get(id=i)
	except Participation.DoesNotExist:
		context = {'message1':'Error', 'message2':'No such event registration exists'}
		return render(request, 'home/message.html', context)

	reg = part.registration_set.all()
	for r in reg:
		r.delete()

	part.delete()

	return HttpResponseRedirect(redirect_to='/home/edit_reg2/?id={}&confirm=t'.format(p))

@login_required(login_url='/login/?loc=home')
def select_event(request):
	events = Event.objects.all().order_by('name')
	context = {'events':events}
	return render(request, 'home/event_list.html', context)


@login_required(login_url='/login/?loc=home')
def get_event_list(request):
	if 'id' in request.GET:
		i = request.GET['id']
	else:
		context = {'message1':'Error', 'message2':'Please provide an event'}
		return render(request, 'home/message.html', context)

	try:
		event = Event.objects.get(id=int(i, 10))
	except Event.DoesNotExist:
		context = {'message1':'Error', 'message2':'No such event occurs. Please add the event first'}
		return render(request, 'home/message.html', context)

	rows = event.participation_set.all()

	buffer = Echo()
	writer = csv.writer(buffer)
	ar = []
	ar.append(['', '', event.name, '', ''])
	ar.append(['', '', '', '', ''])
	ar.append(['CAW ID', '', 'Mobile No', '', 'Name'])
	ar.append(['', '', '', '', ''])
	if event.team is False:
		for row in rows:
			ar.append([row.participent.all()[0].id, '', row.participent.all()[0].phone_no, '', row.participent.all()[0].name])

	else:
		count = 1
		for row in rows:
			ar.append(['', '', '', '', ''])
			ar.append(['Team {}'.format(count), '', '', '', ''])
			count = count+1
			p = row.participent.all()
			for r in p:
				ar.append([r.id, '', r.phone_no, '', r.name])
	
	response = StreamingHttpResponse((writer.writerow(row) for row in ar), content_type="text/csv")
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(event.name)
	return response

@login_required(login_url='/login/?loc=home')
def find_participent_1(request):
	return render(request, 'home/find_participant.html')

@login_required(login_url='/login/?loc=home')
def submit_participent(request):
	if 'id' not in request.GET and 'mob_no' not in request.GET:
		context = {'message1':'Error', 'message2':'Please provide a participent ID or Mobile Number'}
		return render(request, 'home/message.html', context)

	p = None
	if 'id' in request.GET:
		try:
			p = Participent.objects.get(id=int(request.GET['id'], 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'No such participent exists'}
			return render(request, 'home/message.html', context)
	else:
		try:
			p = Participent.objects.get(phone_no=int(request.GET['mob_no'], 10))
		except Participent.DoesNotExist:
			context = {'message1':'Error', 'message2':'No such participent exists'}
			return render(request, 'home/message.html', context)

	a = []
	events = p.participation_set.all().order_by('event')
	for e in events:
		a.append(e.event.name)
	context = {'p':p, 'events':a}
	return render(request, 'home/find_participant_2.html', context)