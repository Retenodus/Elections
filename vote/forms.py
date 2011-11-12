# vim: fileencoding=utf-8 :
from django.conf import settings
from django.forms import Form, ModelForm, RegexField, ModelChoiceField, CharField, EmailField, ValidationError
from elections.vote.models import Election, Electeur

class BulletinForm(Form):

	def __init__(self, *args, **kwargs ):
		super(Form,self).__init__(*args, **kwargs)
		for elect in Election.objects.all():
			self.fields["Election_%s" % elect.slug] = ModelChoiceField (
										label = "%s" % elect.poste, 
										queryset = Electeur.objects.filter(candidat__poste = elect.poste),
										empty_label = "(None)", required = True
										)
	
	def save(self,user):
		print user
		p = user.get_profile()
		p.avote = True
		p.save()
		for name,value in self.cleaned_data.items():
			if name.startswith("Election_"):
				elu = Electeur.objects.get(user__username = value)
				print elu
				elu.nombre_voix += 1
				elu.save()
				#print Electeur.objects.get(user__username = value)[0].nombre_voix
			
