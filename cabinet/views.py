from django.shortcuts import render
from .models import User
from .forms import RegForm, LoginForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
from home.models import Book, Person
from django.db.models.signals import post_save, class_prepared
from django.dispatch import receiver
from requests.exceptions import HTTPError
from django.contrib.auth import logout, authenticate, login

# Create your views here.
def cabinet(request):
	human = get_object_or_404(User, id=request.user.id)
	written = Book.objects.filter(author_name_id=request.user.id)
	read = get_object_or_404(Person, user_id=request.user.id).read.all
	return render(request, "cabinet/cabinet.html", {'user': request.user.is_authenticated, "human": human, "written": written, "read": read})

def addbook(request, book_id):
	print(1)
	book = get_object_or_404(Book, id=book_id)
	user = get_object_or_404(Person, user_id=request.user.id) #Защита от незареганных 
	user.read.add(book)
	return redirect(f"/book/{book_id}")

def reg(request):
	message = ''
	form = RegForm(request.POST or None)
	if form.is_valid():
		form.save()
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password1'])
		login(request, user)
		return redirect('/')
	else:
		try:
			errors = form.errors.as_data()
			messages = [i for i in errors]
			message = str(errors[messages[-1]])
			first = message.find("'") + 1
			second = message.rfind("'") - 1
			message = message[first:second]
		except:
			pass
	return render(request, 'cabinet/registration.html', {'user': request.user.is_authenticated, 'message': message})

def log(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		cd = form.cleaned_data
		user = authenticate(username=cd['username'], password=cd['password'])
		if user is not None:
			login(request, user)
			request.user = 'renat'
			print(request.user, 22)
			return redirect('/')
	return render(request, 'cabinet/login.html', {'user': request.user.is_authenticated, })#

def user_logout(request):
	logout(request)
	return redirect('/')
	

@receiver(post_save, sender = User)
def add_person(instance, **kwargs):
	try:
		person = get_object_or_404(Person, user_id=instance.id) # Если не найдено намерено вызывается ошибка 404
	except:
		person = Person()
		person.user_id = instance.id
		person.save()