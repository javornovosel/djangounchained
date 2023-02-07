from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class CardType(models.Model):
	card_type = models.CharField(max_length = 16, default = 'placeholder', null = True)

	def __str__(self):
		return self.card_type

class Rarity(models.Model): #based on pull rates, maybe add many-to-many CardRarity because it can be both parallel and super rare
	rarity = models.CharField(max_length = 32, default = 'placeholder', unique = True)

	def __str__(self):
		return self.rarity


class CardSet(models.Model):
	set_name = models.CharField(max_length = 128, default = 'placeholder', unique  = True)
	set_id = models.CharField(max_length = 16, default = 'placeholder', unique = True)

	def __str__(self):
		return self.set_name

class Card(models.Model):
	name = models.CharField(max_length = 64)
	card_id = models.CharField(max_length = 10)
	marketprice = models.FloatField()
	image_link = models.CharField(max_length = 64)
	#in_stock = models.BooleanField

	card_color = models.ManyToManyField('Color', through='CardColor')
	card_type = models.ForeignKey(CardType, on_delete=models.CASCADE)
	rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
	card_set = models.ForeignKey(CardSet, on_delete=models.CASCADE)

	def __str__(self):
		return "Card Name :" + str(self.name) + " Card ID: " + str(self.card_id)

class Product(models.Model):
	name = models.CharField(max_length = 100, unique = True)
	marketprice = models.FloatField()
	product_set = models.ForeignKey(CardSet, on_delete= models.CASCADE, default=1)
	user_product = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserProduct', related_name = 'user_product')

class UserProduct(models.Model):
	price_notifications = models.BooleanField(default = False)
	wanted_price = models.FloatField(default = 0)
	highest_value_opened = models.FloatField(default = 0)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'product')


class Color(models.Model):
	card_color = models.ManyToManyField('Card', through='CardColor')
	color = models.CharField(max_length = 12, null = True)

	def __str__(self):
		return self.color

class CardColor(models.Model):
	card = models.ForeignKey(Card, on_delete=models.CASCADE)
	color = models.ForeignKey(Color, on_delete=models.CASCADE)


#class CustomCard(models.Model):
#	name = models.CharField(max_length = 64)
#	attribute = something
#	power = 


