from principal.models import Receta, Comentario
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from principal.forms import ContactoForm, RecetaForm, ComentarioForm
from django.core.mail import EmailMessage

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def sobre(request):
	return render_to_response("acerca_de.html", context_instance=RequestContext(request))

def inicio(request):
	recetas = Receta.objects.all()
	return render_to_response("inicio.html",{"datos" : recetas}, context_instance=RequestContext(request))

def usuarios(request):
	usuarios = User.objects.all()
	recetas = Receta.objects.all()
	return render_to_response("usuarios.html",{"usuarios" : usuarios, "recetas" : recetas }, context_instance=RequestContext(request))

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

def nueva_receta(request):
	if request.method=="POST":
		formulario = RecetaForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect("/recetas")
	else:
		formulario = RecetaForm()

	return render_to_response("receta_form.html", {"formulario" : formulario}, context_instance=RequestContext(request))


def nuevo_comentario(request):
	if request.method=="POST":
		formulario = ComentarioForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect("/recetas")
	else:
		formulario = ComentarioForm()

	return render_to_response("comentario_form.html", {"formulario" : formulario}, context_instance=RequestContext(request))

def nuevo_usuario(request):
	if request.method=="POST":
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect("/")
	else:
		formulario = UserCreationForm()

	return render_to_response("nuevo_usuario.html", {"formulario":formulario}, context_instance=RequestContext(request))

def ingresar(request):
	if not request.user.is_anonymous():
		#logout(request)
		return HttpResponseRedirect("/privado")

	if request.method=="POST":
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST["username"]
			clave = request.POST["password"]
			acceso = authenticate(username = usuario, password = clave)

			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect("/privado")
				else:
					return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/")
		else:
			return HttpResponseRedirect("/")
	else:
		formulario = AuthenticationForm()

	return render_to_response("ingresar.html", {"formulario":formulario}, context_instance=RequestContext(request))

@login_required(login_url="/usuario/ingresar")
def privado(request):
	usuario = request.user
	return render_to_response("privado.html",{"usuario":usuario}, context_instance=RequestContext(request))

@login_required(login_url="/usuario/ingresar")
def cerrar(request):
	logout(request)
	return HttpResponseRedirect("/")

