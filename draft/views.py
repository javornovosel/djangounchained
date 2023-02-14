from django.shortcuts import render
from box.methods import get_random_packs
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