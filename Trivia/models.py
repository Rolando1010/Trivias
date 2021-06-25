from django.db import models
import sqlite3
import random

def conectarSQLite():
    return sqlite3.connect('trivias.sqlite3')

def obtenerTemas():
    conexion = conectarSQLite()
    temas = []
    consulta = conexion.execute('select tema from Temas')
    for fila in consulta:
        temas += [fila[0]]
    conexion.close()
    return temas

def obtenerPreguntasTema(idTema):
    id = 0
    conexion = conectarSQLite()
    consulta = conexion.execute("select id from Temas where tema='"+idTema+"'")
    for fila in consulta:
        id = int(fila[0])
    idsPreguntas = []
    preguntas = []
    consulta = conexion.execute("select id,pregunta from Preguntas where idTema="+str(id))
    for fila in consulta:
        idsPreguntas += [fila[0]]
        preguntas += [fila[1]]
    datos = []
    while(len(idsPreguntas)>0):
        pos = random.randrange(len(idsPreguntas))
        idPregunta = idsPreguntas[pos]
        dato = {}
        dato["pregunta"] = preguntas[pos]
        consulta = conexion.execute("select id,respuesta from Respuestas where idPregunta="+str(idPregunta))
        respuestas = []
        for fila in consulta:
            respuesta = {}
            respuesta["id"] = fila[0]
            respuesta["respuesta"] = fila[1]
            respuestas += [respuesta]
        dato["respuestas"] = respuestas
        datos += [dato]
        idsPreguntas = idsPreguntas[:pos] + idsPreguntas[pos+1:]
        preguntas = preguntas[:pos] + preguntas[pos+1:]
    conexion.close()
    return datos

def crearTrivia(respuestas, nombre, tiempo):
    idUsuario = realizarConsulta("select id from Usuarios where nombre='"+nombre+"'",1)[0][0]
    cantTrivias = realizarConsulta("select count(id) from Trivias where idUsuario="+str(idUsuario),1)[0][0]
    codigoTrivia = "Trivia-"+nombre+"-"+str(cantTrivias+1)
    conexion = conectarSQLite()
    correctos = 0
    for i in range(0,len(respuestas)):
        consulta = realizarConsulta("select id from Correctos where idRespuesta="+respuestas[i],1)
        if consulta!=[]:
            correctos+=1
    conexion.close()
    ejecutarConsulta("insert into Trivias (idUsuario,codigo, puntaje, tiempo) values("+str(idUsuario)+",'"+codigoTrivia+"',"+str(correctos*5)+",'"+tiempo+"')")
    return codigoTrivia

def insertarUsuario(nombre):
    conexion = conectarSQLite()
    id = 0
    consulta = conexion.execute("select id from Usuarios where nombre ='"+nombre+"'")
    for fila in consulta:
        id = fila[0]
    if(id==0):
        conexion.execute("insert into Usuarios (nombre) values ('"+nombre+"')")
        conexion.commit()

def realizarConsulta(consulta, num_datos):
    conexion = conectarSQLite()
    tabla = conexion.execute(consulta)
    datos = []
    for fila in tabla:
        dato = []
        for i in range(0,num_datos):
            dato += [fila[i]]
        datos += [dato]
    conexion.close()
    return datos

def ejecutarConsulta(consulta):
    conexion = conectarSQLite()
    conexion.execute(consulta)
    conexion.commit()

def solicitarDatosTrivia(codigo):
    trivia = realizarConsulta("select idUsuario, tiempo, puntaje from Trivias where codigo='"+codigo+"'",3)[0]
    nombre = realizarConsulta("select nombre from Usuarios where id="+str(trivia[0]),1)[0][0]
    return {"nombre":nombre,"tiempo":trivia[1],"puntaje":trivia[2]}

def generarRanking():
    consulta = realizarConsulta("select b.nombre, a.puntaje, a.tiempo from Trivias a, Usuarios b where a.idUsuario=b.id ORDER by a.puntaje desc",3)
    for i in range(0,len(consulta)):
        consulta[i] = [i+1]+consulta[i]
        consulta[i][-1] += " minutos"
    return consulta