# vim: fileencoding=utf-8 :
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from elections.vote.fields import AutoOneToOneField

class Election(models.Model):
	"""
	Une élection pour chaque poste
	"""
	poste = models.CharField(max_length=20, unique = True)
	slug = models.SlugField(max_length=40, unique = True)
	active = models.BooleanField(default = False)
	elus = models.IntegerField(default = 1)

	def __unicode__(self):
		return self.poste

class Electeur(models.Model):
	""" Profil des utilisateurs """
	user = AutoOneToOneField(User, primary_key = True)
	candidat = models.ForeignKey(Election, blank = True, null = True)
	nombre_voix = models.IntegerField(default = 0)
	avote = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		instance.electeur.avote = False
		instance.save()

post_save.connect(create_user_profile, sender = User)
