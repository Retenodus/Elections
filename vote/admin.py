# vim: fileencoding=utf-8 :
from elections.vote.models import Election, Electeur
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin, GroupAdmin

class UserProfileInline(admin.StackedInline):
	"""
	Permet de rajouter le profil en inline sur l'interface d'administration des utilisateurs
	"""
	model = Electeur
	readonly_fields = ["nombre_voix"]

class UserProfileAdmin(UserAdmin):
	"""
	Remplace la classe d'admin des utilisateurs par défaut avec une
	classe qui inclut les présences en inline
	"""
	inlines = [UserProfileInline]
	list_display = ('username', 'email', 'is_staff', 'candidat', 'nombre_voix', 'avote')
	search_fields = ('username', 'email', 'nombre_voix', 'candidat','avote')

	def nombre_voix(self,obj):
		return obj.get_profile().nombre_voix
	nombre_voix.short_description = "Nombre de voix"

	def candidat(self,obj):
		return obj.get_profile().candidat.poste
	
	def avote(self,obj):
		return obj.get_profile().avote

class ElectionAdmin(admin.ModelAdmin):
	list_display=["poste"]
	prepopulated_fields = {"slug" : ("poste",)}

admin.site.unregister(User)
admin.site.register(User,UserProfileAdmin)
admin.site.register(Election, ElectionAdmin)
