from principal.models import Receta, Comentario
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from principal.forms import ContactoForm
from django.core.mail import EmailMessage

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

def contacto(request):
	if request.method=="POST":
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = "Mensaje desde Recetario"
			contenido = formulario.cleaned_data["mensaje"] + "\n"
			contenido += "Comunicarse a "+ formulario.cleaned_data["correo"]
			correo = EmailMessage(titulo, contenido, to=["eltodi@gmail.com"])
			correo.send()
			return HttpResponseRedirect("/")
	else:
		formulario = ContactoForm()

	return render_to_response("contacto_form.html", {"formulario" : formulario}, context_instance=RequestContext(request))

