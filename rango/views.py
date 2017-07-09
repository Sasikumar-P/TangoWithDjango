from django.shortcuts import render
from rango.models import Category
from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout



def index(request):

	context_dict = {'boldmessage': "I am bold font from the context"}
	category_list = Category.objects.order_by('-name')[:5]
	print category_list
	context_dict = {'categories': category_list}
	return render(request, 'index.html', context_dict)

def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST) 
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
            		profile.user = user
			if 'picture' in request.FILES:
                		profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors

	else:
		user_form = UserForm()
        	profile_form = UserProfileForm()

	return render(request,'register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
        	password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
                		return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your Rango account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
            		return HttpResponse("Invalid login details supplied.")
	else:
		 return render(request, 'login.html', {})


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')
#Create your views here.
