from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.mixins import LoginRequiredMixin

from box.methods import get_average, get_minimum, get_random_packs
from box.models import Product, UserProduct
from box.forms import SignupForm

def my_callback(sender):
	print("something happens")
	
class MainView(View):
	def get(self, request):
		chosen_set = 'Romance Dawn'
		average_box_value = get_average(chosen_set)
		minimal_box_value = get_minimum(chosen_set)

		cntx = {
				'average_box_value' : average_box_value,
				'minimal_box_value' : minimal_box_value,
				}

		return render(request, 'box/main.html', cntx)#reverse dodaj


class AddNotificationView(LoginRequiredMixin, View):
	def get(self, request):#figure out why cardset doesn't work right
		notify_list = UserProduct.objects.filter(user=request.user, price_notifications=True).values('product__name', 'wanted_price')
		product_list = Product.objects.exclude(product_set = 24).values('name', 'marketprice').order_by('name')#exclude promo karte

		cntx = {
				'product_list' : product_list,
				'notify_list':notify_list
				}

		return render(request, 'box/notify.html', cntx)

	def post(self, request):
		product = get_object_or_404(Product, name=request.POST['tracked_product'])
		up, created = UserProduct.objects.get_or_create(user=request.user, product=product)

		if not created:
			up.wanted_price = request.POST['wanted_price']
			up.price_notifications = True
			up.save()

		else:
			up.price_notifications = True
			up.wanted_price = request.POST['wanted_price']
			up.save()

		return redirect(reverse_lazy('box:notify'))


def remove_notification(request, product__name):
	product = get_object_or_404(Product, name=product__name)#vjerojatno postoji način da se referiram na to u notificationu
	notification = get_object_or_404(UserProduct, user=request.user, product=product)
	notification.price_notifications = False
	notification.wanted_price = 0
	notification.save()
	return redirect(reverse_lazy('box:notify'))


class OpeningView(View):
	def get(self, request, chosen_set = None, number_of_packs = None):
		if number_of_packs == None:
			number_of_packs = 24
		else:
			number_of_packs = int(number_of_packs)

		if chosen_set == None:
			chosen_set = 'Romance Dawn'
		
		number_of_packs = int(request.GET.get('number_of_packs', number_of_packs))
		random_packs = get_random_packs(chosen_set, number_of_packs)

		card_list = random_packs['card_list']
		total_value = random_packs['total_value']
		card_count = len(card_list)

		highest_ever = UserProduct.objects.values('highest_value_opened').order_by('-highest_value_opened')[0]


		if request.user.is_anonymous is False:#vjerojatno ima bolji način
			product_opened = get_object_or_404(Product, name=f'{chosen_set} Booster Box')
			current_highest, created = UserProduct.objects.get_or_create(user=request.user, product=product_opened)
			if current_highest.highest_value_opened < total_value:
				current_highest.highest_value_opened = total_value
				current_highest.save()
				current_highest = current_highest.highest_value_opened


		else:
			current_highest = None

		cntx = {
				'card_list' : card_list,
				'card_count' : card_count,
				'total_value' : total_value,
				'highest_ever': highest_ever['highest_value_opened'],
				'highest_value':current_highest
				}

		return render(request, 'box/opening.html', cntx)


class SignupView(CreateView):
	model = User
	success_url = reverse_lazy('box:main')
	template_name = 'registration/signup.html'

	def get(self, request):
		form = SignupForm()
		context = {'form':form}
		return render(request, self.template_name, context)

	def post(self, request):
		form = SignupForm(request.POST)
		if not form.is_valid():
			return render(request, self.template_name, {'form':form})

		new_user = form.save()
		new_user = authenticate(username=form.cleaned_data['username'],
								password=form.cleaned_data['password1'],)
		login(request, new_user)

		return redirect(self.success_url)

#class CreateCard(View):

#23 DON!!
#1 box topper
#1 alternate DON
#168 common
#72 uncommon - 8 leader = 64 uncommon
#24 rare - 8.34 super rare or greater = 15.66 rare
#1 parallel
#0.67 secret rare 
#0.33 alternate leader 
#0.0083 manga

#nadogradnje
#pack opening-box opening, highest value box opened on site
#draft? imam random_packs
#auto-update baze podataka jednom dnevno
#notify mailom kad x karta ili box value padne ispod unesenih podataka
#hover iznad prouvoda u notify prikaže sliku
#list of cards, ability to search and filter 
#zasebna baza koja prati dnevno kretanje (vjerojatno u jsonu)
#createa-a-card