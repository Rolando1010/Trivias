from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("<nombre>/temas",views.temas,name="temas"),
    path("<nombre>/<tema>/pregunta",views.pregunta,name="pregunta"),
    path("resultado/<trivia>",views.resultado,name="resultado"),
    path("ranking",views.ranking,name="ranking")
]