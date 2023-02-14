from box.models import Card, Rarity, CardSet
from django.db.models import Avg, Sum
from random import choice
import random

def get_average(chosen_set):
	don = Card.objects.filter(rarity__rarity = 'DON!!', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))#dictionary {'marketprice' :marketprice}
	alternate_don = Card.objects.filter(rarity__rarity = 'Alternate DON!!', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))#only 1 don so no need to average
	common = Card.objects.filter(rarity__rarity = 'Common', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	uncommon = Card.objects.filter(rarity__rarity = 'Uncommon', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	leader = Card.objects.filter(rarity__rarity = 'Leader', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	rare = Card.objects.filter(rarity__rarity = 'Rare', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	super_rare = Card.objects.filter(rarity__rarity = 'Super Rare', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	secret_rare = Card.objects.filter(rarity__rarity = 'Secret Rare', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	box_topper = Card.objects.filter(rarity__rarity = 'Box Topper', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	parallel = Card.objects.filter(rarity__rarity = 'Parallel', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	alternate_leader = Card.objects.filter(rarity__rarity = 'Alternate Leader', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))
	manga = Card.objects.filter(rarity__rarity = 'Manga', card_set__set_name = chosen_set).values('marketprice').aggregate(Avg('marketprice'))#only 1 manga no average needed

	#avg_box_topper = objects.aggregate(Avg('wins'))
	#{'price__avg': 34.35}
	#random_boxtopper = random.choice(list(box_topper.values()))

	#key = choice(list(deck))
	#value = deck.pop(key)

	average_box_value = 23 * don['marketprice__avg'] + alternate_don['marketprice__avg'] + box_topper['marketprice__avg'] + 168 * common['marketprice__avg'] + 64 * uncommon['marketprice__avg'] + 8 * leader['marketprice__avg'] + 15.66 * rare['marketprice__avg']
	average_box_value = average_box_value + 6.332 * super_rare['marketprice__avg'] + parallel['marketprice__avg'] + 0.67 * secret_rare['marketprice__avg'] + 0.33 * alternate_leader['marketprice__avg'] + 0.008 * manga['marketprice__avg']
	#nisam ziher kak staviti da ne bu u jednom redu

	return average_box_value

def get_minimum(chosen_set):

	don = Card.objects.filter(rarity__rarity = 'DON!!', card_set__set_name = chosen_set).values('marketprice')[0] #dictionary {'marketprice' :marketprice}
	alternate_don = Card.objects.filter(rarity__rarity = 'Alternate DON!!', card_set__set_name = chosen_set).values('marketprice')[0]
	common = Card.objects.filter(rarity__rarity = 'Common', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0:42].aggregate(Sum('marketprice'))
	uncommon = Card.objects.filter(rarity__rarity = 'Uncommon', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0:32].aggregate(Sum('marketprice'))
	leader = Card.objects.filter(rarity__rarity = 'Leader', card_set__set_name = chosen_set).values('marketprice').aggregate(Sum('marketprice'))#all leader summed
	rare = Card.objects.filter(rarity__rarity = 'Rare', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0:8].aggregate(Sum('marketprice'))
	super_rare = Card.objects.filter(rarity__rarity = 'Super Rare', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0:6].aggregate(Sum('marketprice'))
	secret_rare = Card.objects.filter(rarity__rarity = 'Secret Rare', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0]
	box_topper = Card.objects.filter(rarity__rarity = 'Box Topper', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0]
	parallel = Card.objects.filter(rarity__rarity = 'Parallel', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0]
	alternate_leader = Card.objects.filter(rarity__rarity = 'Alternate Leader', card_set__set_name = chosen_set).values('marketprice').order_by('marketprice')[0]

	if secret_rare['marketprice'] > alternate_leader['marketprice']:
		secret_or_leader = alternate_leader['marketprice']
	else:
		secret_or_leader = secret_rare['marketprice']


	minimal_box_value = 23 * don['marketprice'] + alternate_don['marketprice'] + leader['marketprice__sum'] + box_topper['marketprice'] + 4 * common['marketprice__sum']
	minimal_box_value = minimal_box_value + 2 * uncommon['marketprice__sum'] +  2 * rare['marketprice__sum']	+ super_rare['marketprice__sum'] + parallel['marketprice'] + secret_or_leader
	
	return minimal_box_value


def get_random_packs(chosen_set, number_of_packs, draft = False):

	cards_pulled = []
	cards_opened = {}#rename, too similar to cards_pulled
	pack_list = []
	total_value = 0

	leader = Card.objects.filter(rarity__rarity = 'Leader', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
	super_rare = Card.objects.filter(rarity__rarity = 'Super Rare', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
	secret_rare = Card.objects.filter(rarity__rarity = 'Secret Rare', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
	box_topper = Card.objects.filter(rarity__rarity = 'Box Topper', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
	parallel = Card.objects.filter(rarity__rarity = 'Parallel', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
	alternate_leader = Card.objects.filter(rarity__rarity = 'Alternate Leader', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
	manga = Card.objects.filter(rarity__rarity = 'Manga', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')

	for i in range(number_of_packs):
		if draft == True:
			cards_pulled = []

		don = Card.objects.filter(rarity__rarity = 'DON!!', card_set__set_name = chosen_set).values('marketprice', 'name','image_link')
		alternate_don = Card.objects.filter(rarity__rarity = 'Alternate DON!!', card_set__set_name = chosen_set).values('marketprice', 'name','image_link')
		common = Card.objects.filter(rarity__rarity = 'Common', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
		uncommon = Card.objects.filter(rarity__rarity = 'Uncommon', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')
		rare = Card.objects.filter(rarity__rarity = 'Rare', card_set__set_name = chosen_set).values('marketprice', 'name','image_link', 'card_id')


		for i in range(7):#random.choices can get multiple unique cards random.choice(common, k=3), but each cards needs a ['count'] and to be added to cards_opened
			random_common = random.choice(common)#i can make it a method, but it takes more database yoinks
			random_common['count'] = 1
			cards_opened[random_common['card_id']] = cards_opened.get(random_common['card_id'], 0) + 1
			if random_common not in cards_pulled:
				cards_pulled.append(random_common)
			common = common.exclude(card_id = random_common['card_id'])
			total_value = total_value + random_common['marketprice']


		for i in range(3):

			leader_lottery = random.randrange(1,10)

			if leader_lottery == 1:
				try:
					random_leader = random.choice(leader)
					random_leader['count'] = 1
					if random_leader not in cards_pulled:
						cards_pulled.append(random_leader)
					leader = leader.exclude(card_id = random_leader['card_id'])
					total_value = total_value + random_leader['marketprice']
				except:
					random_uncommon = random.choice(uncommon)
					random_uncommon['count'] = 1
					cards_opened[random_uncommon['card_id']] = cards_opened.get(random_uncommon['card_id'], 0) + 1
					if random_uncommon not in cards_pulled:
						cards_pulled.append(random_uncommon)
					uncommon = uncommon.exclude(card_id = random_uncommon['card_id'])
					total_value = total_value + random_uncommon['marketprice']



			else:
				random_uncommon = random.choice(uncommon)
				random_uncommon['count'] = 1
				cards_opened[random_uncommon['card_id']] = cards_opened.get(random_uncommon['card_id'], 0) + 1
				if random_uncommon not in cards_pulled: 
					cards_pulled.append(random_uncommon)
				uncommon = uncommon.exclude(card_id = random_uncommon['card_id'])
				total_value = total_value + random_uncommon['marketprice']

		random_rare = random.choice(rare)#this all could be one method i call instead of typing it out like a dumbo
		random_rare['count'] = 1
		cards_opened[random_rare['card_id']] = cards_opened.get(random_rare['card_id'], 0) + 1
		if random_rare not in cards_pulled: 
			cards_pulled.append(random_rare)
		rare = rare.exclude(card_id = random_rare['card_id'])
		total_value = total_value + random_rare['marketprice']


		manga_lottery = random.randrange(1,34501)
		alternate_leader_lottery = random.randrange(1,73)
		secret_rare_lottery = random.randrange(1,37)
		parallel_lottery = random.randrange(1,25)
		super_rare_lottery = random.randrange(1,5)

		if manga_lottery == 1:

			try:#in case someone pulls two manga cards
				random_manga = random.choice(manga)
				random_manga['count'] = 1
				cards_pulled.append(random_manga)#znam da je blesavo al ga pretvara iz quertype u dict
				manga = manga.exclude(card_id)
				total_value = total_value + random_manga['marketprice']

			except:
				random_alternate_leader = random.choice(alternate_leader)
				random_alternate_leader['count'] = 1
				cards_pulled.append(random_alternate_leader)
				alternate_leader = alternate_leader.exclude(card_id = random_alternate_leader['card_id'])
				total_value = total_value + random_alternate_leader['marketprice']

		elif alternate_leader_lottery == 1:

			random_alternate_leader = random.choice(alternate_leader)
			random_alternate_leader['count'] = 1
			cards_pulled.append(random_alternate_leader)
			alternate_leader = alternate_leader.exclude(card_id = random_alternate_leader['card_id'])
			total_value = total_value + random_alternate_leader['marketprice']

		elif secret_rare_lottery == 1:

			try:#in case someone pulls three secret rares
				random_secret_rare = random.choice(secret_rare)
				random_secret_rare['count'] = 1
				cards_pulled.append(random_secret_rare)
				secret_rare = secret_rare.exclude(card_id = random_secret_rare['card_id'])
				total_value = total_value + random_secret_rare['marketprice']

			except:
				random_parallel = random.choice(parallel)
				random_parallel['count'] = 1
				cards_pulled.append(random_parallel)
				parallel = parallel.exclude(card_id = random_parallel['card_id'])
				total_value = total_value + random_parallel['marketprice']


		elif parallel_lottery == 1:


			random_parallel = random.choice(parallel)
			random_parallel['count'] = 1
			cards_pulled.append(random_parallel)
			parallel = parallel.exclude(card_id = random_parallel['card_id'])
			total_value = total_value + random_parallel['marketprice']



		elif super_rare_lottery == 1:

			random_super_rare = random.choice(super_rare)
			random_super_rare['count'] = 1
			if random_super_rare not in cards_pulled:
				cards_pulled.append(random_super_rare)
			super_rare = super_rare.exclude(card_id = random_super_rare['card_id'])
			total_value = total_value + random_super_rare['marketprice']


		else:

			random_rare = random.choice(rare)#this all could be one method i call instead of typing it out like a dumbo
			random_rare['count'] = 1
			cards_opened[random_rare['card_id']] = cards_opened.get(random_rare['card_id'], 0) + 1
			if random_rare not in cards_pulled: 
				cards_pulled.append(random_rare)
			total_value = total_value + random_rare['marketprice']

		if draft == True:
			pack_list.append(cards_pulled)

	if draft == True:
		return pack_list

	for i in range(len(cards_pulled)):
		for k,v in cards_opened.items():
			if cards_pulled[i]['card_id'] == k:
				cards_pulled[i]['count'] = v
			else: continue




	return {'total_value' : total_value, 'card_list' : sorted(cards_pulled, key=lambda d: d['marketprice'], reverse = True)}







#23 DON!!
#1 box topper
#1 alternate DON
#168 common
#72 uncommon - 8 leader = 64 uncommon 1 out of 9 leader
#24 rare - 8.34 super rare or greater = 15.66 rare
#1 parallel, 1 in 24
#0.67 secret rare, 1 in 36 packs
#0.33 alternate leader, 1 in 72 packs
#0.0083 manga = 3.45 * 10 na-4


