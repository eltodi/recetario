from principal.models import Receta, Comentario
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User

def sobre(request):
	return render_to_response("acerca_de.html")

def inicio(request):
	recetas = Receta.objects.all()
	return render_to_response("inicio.html",{"datos" : recetas})

def usuarios(request):
	usuarios = User.objects.all()
	recetas = Receta.objects.all()
	return render_to_response("usuarios.html",{"usuarios" : usuarios, "recetas" : recetas })

def recetas(request):
	recetas = Receta.objects.all()
	return render_to_response("recetas.html", {"recetas" : recetas}, context_instance=RequestContext(request))

def detalle_receta(request, id_receta):
	receta = get_object_or_404(Receta, pk=id_receta)
	comentarios = Comentario.objects.filter(receta=receta)
	return render_to_response("receta.html", {"receta" : receta, "comentarios" : comentarios}, context_instance=RequestContext(request))	
