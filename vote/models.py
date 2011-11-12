# vim: fileencoding=utf-8 :
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _

class Election(models.Model):
	"""
	Une élection pour chaque poste
	"""
	poste = models.CharField(max_length=20, unique = True)
	slug = models.SlugField(max_length=40, unique = True)

	def __unicode__(self):
		return self.poste

class Electeur(models.Model):
	""" Profil des utilisateurs """
	user = models.ForeignKey(User, unique = True)
	candidat = models.ForeignKey(Election, blank = True, null = True)
	nombre_voix = models.IntegerField(default = 0)
	avote = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username
