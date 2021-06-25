from django.shortcuts import render, redirect
from .models import obtenerTemas, obtenerPreguntasTema, crearTrivia, insertarUsuario, solicitarDatosTrivia, generarRanking

def index(request):
    if request.method == "POST":
        nombre = request.POST["nombre"]
        insertarUsuario(nombre)
        return redirect("/"+nombre+"/temas")
    return render(request,"index.html")

def temas(request,nombre):
    if request.method == "POST":
        tema = request.POST["tema"]
        return redirect("/"+nombre+"/"+tema+"/pregunta")
    return render(request,"temas.html",{"temas":obtenerTemas()})

def pregunta(request,nombre,tema):
    if request.method == "POST":
        codigo = crearTrivia(request.POST["respuestas"].split("|")[::-1][1:][::-1], nombre, request.POST["tiempo"])
        return redirect("/resultado/"+codigo)
    return render(request,"pregunta.html",{"datos":obtenerPreguntasTema(tema)})

def resultado(request,trivia):
    return render(request,"resultado.html",solicitarDatosTrivia(trivia))

def ranking(request):
    return render(request,"ranking.html",{"filas":generarRanking()})