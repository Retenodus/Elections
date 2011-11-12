# vim: fileencoding=utf-8 :

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from elections.vote.forms import BulletinForm

@login_required
def bulletin(request):
	""" Permet de voter """
	
	p = request.user.get_profile()
	if p.avote == True:
		return redirect('vote-dejavote')

	if request.method == "POST":
		form = BulletinForm(request.POST)
		if form.is_valid():
			form.save(request.user)
			return redirect('vote-avote')
	else :
		form = BulletinForm()
	
	return render_to_response("vote/bulletin.html", {"form": form, }, RequestContext(request))
