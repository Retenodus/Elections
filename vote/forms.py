# vim: fileencoding=utf-8 :
from django.conf import settings
from django.forms import Form, ModelForm, RegexField, ModelChoiceField, CharField, ValidationError, BooleanField, MultipleChoiceField
from elections.vote.models import Election, Electeur
import settings

class BulletinForm(Form):

	def __init__(self, *args, **kwargs ):

		self.elects = kwargs.pop('elects', None)
		super(Form,self).__init__(*args, **kwargs)
		for elect in self.elects:
			self.fields["Election_%s" % elect.slug] = MultipleChoiceField (
		label = "%s (maximum %s elu(s))" % (elect.poste, str(elect.elus)), 
		choices = [(e.user.username,e.user.username) for e in Electeur.objects.filter(candidat__poste = elect.poste)] + [("Blanc","Blanc")],
		required = True
										)
		self.fields["Validation"] = BooleanField (
										label = "JE VALIDE MON VOTE (ACTION IRRÉVERSIBLE) !")
	
	def clean_Validation(self):
		data = self.cleaned_data["Validation"]
		if not data :
			raise ValidationError("Vous n'avez pas confirmé votre choix")
		return data

	def clean(self):
		for elect in self.elects:
			data = self.cleaned_data["Election_%s" % elect.slug]
			if len(data) > elect.elus :
				raise ValidationError("Veuillez respecter le nombre maximum de personnes pour qui vous votez")
		return self.cleaned_data

	
	def save(self,user):
		print user
		p = user.get_profile()
		p.avote = True
		p.save()
		rfile = open(settings.BULLETINS + "/elections.txt","a")
		for name,values in self.cleaned_data.items():
			if name.startswith("Election_"):
				for v in values :
					rfile.write(name + " : " + v + "\n")
					if v != "Blanc":
						elu = Electeur.objects.get(user__username = v)
						elu.nombre_voix += 1
						elu.save()
		#				#print Electeur.objects.get(user__username = value)[0].nombre_voix
		rfile.write("\n----------\n")
		rfile.close()
			
