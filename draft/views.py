from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from box.methods import get_random_packs
from box.models import Card, Draft




# Create your views here.
def lobby(request):
	return render(request, 'draft/lobby.html')

def asynclobby(request, room_name):
	chosen_set = 'Romance Dawn'
	pack_list = get_random_packs(chosen_set, 24, True)

	cntx = {
		'room_name' : room_name,
		'pack_list' : pack_list
			}

	return render(request, 'draft/lobby.html', cntx )

def add_card(request, card_id, room_name):#vjerojatno ima elegantniji način, tipa korišternje card_id i card_rarity
	try:
		card = get_object_or_404(Card, card_id=card_id)
	except MultipleObjectsReturned:
		card = Card.objects.filter(card_id=card_id).first()

	draft, created = Draft.objects.get_or_create(user=request.user, card=card)

	if not created:
		draft.count += 1

	else:
		draft.count = 1

	draft.save()#mogu na temelju class pack-container active odrediti koji card_id micati ukoliko ima više karti s istim ID
	#možda moram i lokalno maknuti odabranu kartu i prek websocketa, tak da ak osoba nebre brzo par puta kliknuti

	return HttpResponse(status = 200)

def remove_notification(request, product__name):
	product = get_object_or_404(Product, name=product__name)#vjerojatno postoji način da se referiram na to u notificationu
	notification = get_object_or_404(UserProduct, user=request.user, product=product)
	notification.price_notifications = False
	notification.wanted_price = 0
	notification.save()
	return redirect(reverse_lazy('box:notify'))