# vim: fileencoding=utf-8 :
from django.conf import settings
from django.forms import Form, ModelForm, RegexField, ModelChoiceField, CharField, EmailField, ValidationError, BooleanField
from elections.vote.models import Election, Electeur
import settings

class BulletinForm(Form):

	def __init__(self, elects, *args, **kwargs ):
		super(Form,self).__init__(*args, **kwargs)
		for elect in elects:
			self.fields["Election_%s" % elect.slug] = ModelChoiceField (
										label = "%s" % elect.poste, 
										queryset = Electeur.objects.filter(candidat__poste = elect.poste),
										empty_label = "Blanc", required = False
										)
		self.fields["Validation"] = BooleanField (
										label = "JE VALIDE MON VOTE (ACTION IRRÉVERSIBLE) !")
	
	def clean_Validation(self):
		data = self.cleaned_data["Validation"]
		if not data :
			raise forms.ValidationError("Vous n'avez pas confirmé votre choix")
		return data

	
	def save(self,user):
		print user
		p = user.get_profile()
		p.avote = True
		p.save()
		for name,value in self.cleaned_data.items():
			if name.startswith("Election_"):
				rfile = open(settings.BULLETIN + "/" + name,"r")
				rfile.write(name + " : " + value + "\n")
				rfile.close()
				if value :
					elu = Electeur.objects.get(user__username = value)
					elu.nombre_voix += 1
					elu.save()
				#print Electeur.objects.get(user__username = value)[0].nombre_voix
			
